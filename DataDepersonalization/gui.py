import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox, filedialog

import pandas as pd

from io_utils import load_dataset, save_dataset
from anonymizer import anonymize, METHOD_TEXT
from kanon import k_report
from metrics import field_metrics, stats_compare, table_text

GRAY = "#808080"
CODE_DIR = os.path.dirname(os.path.abspath(__file__))  # папка с кодом


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Обезличивание данных")
        self.geometry("1000x720")
        # системный моноширинный шрифт: таблицы в окне выравниваются по столбцам на любой ОС
        self.mono = tkfont.nametofont("TkFixedFont").copy()
        self.mono.configure(size=12)
        self.report_callback_exception = lambda *a: messagebox.showerror("Ошибка", str(a[1]))

        self.orig = None   # исходный датасет
        self.anon = None   # обезличенный датасет
        self.info = None   # информация об обезличивании (методы, aligned, ...)
        self.loaded_path = None
        self.vars = {}     # столбец -> BooleanVar (чекбокс «обезличивать»)

        # панель кнопок
        bar = tk.Frame(self)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        for text, cmd in [("обезличить", self.run_anonymize),
                          ("рассчитать k-anonymity", self.calc_k),
                          ("оценить полезность", self.utility),
                          ("сохранить результат", self.save),
                          ("выход", self.destroy)]:
            tk.Button(bar, text=text, command=cmd).pack(side="left", padx=2, pady=2)

        self.columnconfigure((0, 1), weight=1, uniform="c")
        self.rowconfigure(2, weight=1)

        self.label("Выберите, что обезличивать", 1, 0)
        self.label("Топ плохих k anonymity / результаты", 1, 1)

        self.checks = tk.Frame(self)
        self.checks.grid(row=2, column=0, sticky="nsew", padx=5)
        self.out = tk.Text(self, font=self.mono, wrap="none")
        self.out.grid(row=2, column=1, sticky="nsew")

        self.label("имя файла ввода (исходные данные)", 3, 0)
        self.label("имя файла вывода", 3, 1)
        self.in_name = self.path_row(4, 0, self.pick_input)
        self.out_name = self.path_row(4, 1, self.pick_output)
        self.out_name.insert(0, "Depersonalization.xlsx")

        self.label("файл для K-anonymity (необязательно, любой датасет; пусто = текущие данные)", 5, 0, span=2)
        self.k_name = self.path_row(6, 0, self.pick_k, span=2)

    # ---------- построение окна ----------
    def label(self, text, row, col, span=1):
        tk.Label(self, text=text, bg=GRAY, fg="white", font=("Arial", 13), pady=8)\
            .grid(row=row, column=col, columnspan=span, sticky="ew")

    def path_row(self, row, col, command, span=1):
        frame = tk.Frame(self)
        frame.grid(row=row, column=col, columnspan=span, sticky="ew")
        entry = tk.Entry(frame, justify="center", font=("Arial", 13))
        entry.pack(side="left", fill="x", expand=True)
        tk.Button(frame, text="Обзор...", command=command).pack(side="right")
        return entry

    def build_checks(self, columns):
        # чекбокс на каждый столбец исходного набора; по умолчанию обезличиваем всё
        old = {c: v.get() for c, v in self.vars.items()}
        for w in self.checks.winfo_children():
            w.destroy()
        self.vars = {}
        for col in columns:
            var = tk.BooleanVar(value=old.get(col, True))
            tk.Checkbutton(self.checks, text=f"{col}  —  {METHOD_TEXT.get(col, 'нет метода')}",
                           variable=var, font=("Arial", 12), wraplength=440, justify="left")\
                .pack(anchor="w")
            self.vars[col] = var

    def show(self, text):
        self.out.delete("1.0", "end")
        self.out.insert("1.0", text)

    # ---------- выбор файлов ----------
    def pick(self, entry, title):
        path = filedialog.askopenfilename(title=title, filetypes=[("Таблицы", "*.xlsx *.csv"), ("Все файлы", "*.*")])
        if path:
            entry.delete(0, "end")
            entry.insert(0, path)
        return path

    def pick_input(self):
        if self.pick(self.in_name, "Выберите исходную таблицу"):
            self.ensure_loaded()  # сразу загружаем и показываем столбцы

    def pick_k(self):
        self.pick(self.k_name, "Датасет для расчёта K-anonymity")

    def pick_output(self):
        path = filedialog.asksaveasfilename(title="Куда сохранить", defaultextension=".xlsx",
                                            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")])
        if path:
            self.out_name.delete(0, "end")
            self.out_name.insert(0, path)

    def ensure_loaded(self):
        path = self.in_name.get().strip()
        if not path:
            raise ValueError("Укажите файл ввода")
        if self.orig is None or path != self.loaded_path:
            self.orig = load_dataset(path)
            self.anon = self.info = None
            self.loaded_path = path
            self.build_checks(self.orig.columns)

    # ---------- кнопки ----------
    def run_anonymize(self):
        self.ensure_loaded()
        selected = [c for c, v in self.vars.items() if v.get()]
        self.anon, self.info = anonymize(self.orig, selected)
        i = self.info

        if i["reached"]:
            lines = [f"Обезличено. K >= {i['k']} по всем полям результата."]
        else:
            lines = [f"Строки не удалялись: для K >= {i['k']} пришлось бы удалить {i['share'] * 100:.1f}% (больше 10%)."]
        lines += ["", "Методы по полям:"]
        lines += [f"  {c}: {m}" for c, m in i["methods"].items()]
        lines += ["", f"Строк: {len(self.orig)} -> {len(self.anon)} "
                      f"(удалено {i['deleted']}, {i['deleted'] / len(self.orig) * 100:.1f}%)",
                  "", "=== K-anonymity обезличенного набора (в любом случае) ===", ""]
        lines += k_report(self.anon, "обезличенный")
        lines += ["", "«сохранить результат» запишет файл."]
        self.show("\n".join(lines))

    def calc_k(self):
        # K-anonymity по всем полям: любой датасет из поля «файл для K-anonymity», иначе текущие данные
        path = self.k_name.get().strip()
        if path:
            df, name = load_dataset(path), os.path.basename(path)
        elif self.anon is not None:
            df, name = self.anon, "обезличенный (текущий)"
        else:
            self.ensure_loaded()
            df, name = self.orig, "исходный (текущий)"
        self.show("\n".join(k_report(df, name)))

    def utility(self):
        if self.anon is None:
            return messagebox.showwarning("Внимание", "Сначала обезличьте датасет")
        table = field_metrics(self.orig, self.info["aligned"], self.anon, self.info["methods"])
        lines = ["Метрики по всем полям:", table_text(table),
                 "",
                 "KLD = 0: распределение не изменилось. Для обобщённых полей оригинал приводится",
                 "к тому же виду, поэтому потерю информации там показывают «уник. до / после»."]
        num = [c for c in self.anon.columns if c in self.orig.columns
               and pd.api.types.is_numeric_dtype(self.anon[c]) and pd.api.types.is_numeric_dtype(self.orig[c])]
        if num:
            lines += ["", "Статистика числовых полей до / после:", stats_compare(self.orig, self.anon, num).round(2).to_string()]
        self.show("\n".join(lines))

    def save(self):
        if self.anon is None:
            return messagebox.showwarning("Внимание", "Сначала обезличьте датасет")
        # относительное имя -> в папку с кодом; абсолютный путь (из «Обзор») остаётся как есть
        path = os.path.join(CODE_DIR, self.out_name.get())
        save_dataset(self.anon, path)
        messagebox.showinfo("Готово", f"Сохранено: {path}")


if __name__ == "__main__":
    App().mainloop()
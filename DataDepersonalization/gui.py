import os
import tkinter as tk
from tkinter import messagebox, filedialog

from io_utils import load_dataset, save_dataset
from anonymizer import anonymize, generalize_coords, generalize_datetime, generalize_quantity, COORD_DECIMALS
from kanon import k_per_row, top_bad_k, unique_rows, required_k
from metrics import kld_column, stats_compare

GRAY = "#808080"
CODE_DIR = os.path.dirname(os.path.abspath(__file__))  # папка с кодом
DIRECT_IDS = ("card_number", "receipt_number")  # по умолчанию не выбираем в квази-идентификаторы


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Обезличивание данных")
        self.geometry("950x650")
        self.report_callback_exception = lambda *a: messagebox.showerror("Ошибка", str(a[1]))

        self.orig = None   # исходный датасет
        self.anon = None   # обезличенный датасет
        self.loaded_path = None
        self.vars = {}     # столбец -> BooleanVar (чекбокс)

        # панель кнопок
        bar = tk.Frame(self)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        for text, cmd in [("рассчитать k-anonymity", self.calc_k),
                          ("обезличить", self.run_anonymize),
                          ("оценить полезность", self.utility),
                          ("сохранить результат", self.save),
                          ("выход", self.destroy)]:
            tk.Button(bar, text=text, command=cmd).pack(side="left", padx=2, pady=2)

        # сетка: заголовки / чекбоксы + вывод / подписи файлов / поля файлов
        self.columnconfigure((0, 1), weight=1, uniform="c")
        self.rowconfigure(2, weight=1)

        tk.Label(self, text="Выберите квази идентификаторы", bg=GRAY, fg="white",
                 font=("Arial", 13), pady=8).grid(row=1, column=0, sticky="ew")
        tk.Label(self, text="Топ плохих k anonymity", bg=GRAY, fg="white",
                 font=("Arial", 13), pady=8).grid(row=1, column=1, sticky="ew")

        self.checks = tk.Frame(self)
        self.checks.grid(row=2, column=0, sticky="nsew", padx=5)
        self.out = tk.Text(self, font=("Consolas", 11), wrap="none")
        self.out.grid(row=2, column=1, sticky="nsew")

        tk.Label(self, text="имя файла ввода", bg=GRAY, fg="white",
                 font=("Arial", 13), pady=8).grid(row=3, column=0, sticky="ew")
        tk.Label(self, text="имя файла вывода", bg=GRAY, fg="white",
                 font=("Arial", 13), pady=8).grid(row=3, column=1, sticky="ew")

        # поля с путями + кнопки «Обзор»
        in_row = tk.Frame(self)
        in_row.grid(row=4, column=0, sticky="ew")
        self.in_name = tk.Entry(in_row, justify="center", font=("Arial", 13))
        self.in_name.pack(side="left", fill="x", expand=True)
        tk.Button(in_row, text="Обзор...", command=self.pick_input).pack(side="right")

        out_row = tk.Frame(self)
        out_row.grid(row=4, column=1, sticky="ew")
        self.out_name = tk.Entry(out_row, justify="center", font=("Arial", 13))
        self.out_name.insert(0, "Depersonalization.xlsx")
        self.out_name.pack(side="left", fill="x", expand=True)
        tk.Button(out_row, text="Обзор...", command=self.pick_output).pack(side="right")

    # ---------- выбор файлов ----------
    def pick_input(self):
        path = filedialog.askopenfilename(
            title="Выберите исходную таблицу",
            filetypes=[("Таблицы", "*.xlsx *.csv"), ("Все файлы", "*.*")])
        if path:
            self.in_name.delete(0, "end")
            self.in_name.insert(0, path)
            self.ensure_loaded()  # сразу загружаем и показываем столбцы

    def pick_output(self):
        path = filedialog.asksaveasfilename(
            title="Куда сохранить", defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx")])
        if path:
            self.out_name.delete(0, "end")
            self.out_name.insert(0, path)

    # ---------- вспомогательное ----------
    def show(self, text):
        self.out.delete("1.0", "end")
        self.out.insert("1.0", text)

    def build_checks(self, df):
        # чекбоксы по столбцам текущего датасета, прежний выбор сохраняем
        old = {c: v.get() for c, v in self.vars.items()}
        for w in self.checks.winfo_children():
            w.destroy()
        self.vars = {}
        for col in df.columns:
            var = tk.BooleanVar(value=old.get(col, col not in DIRECT_IDS))
            tk.Checkbutton(self.checks, text=col, variable=var,
                           font=("Arial", 12)).pack(anchor="w")
            self.vars[col] = var

    def ensure_loaded(self):
        path = self.in_name.get()
        if self.orig is None or path != self.loaded_path:
            self.orig = load_dataset(path)
            self.anon = None
            self.loaded_path = path
            self.build_checks(self.orig)

    def current(self):
        return self.anon if self.anon is not None else self.orig

    # ---------- команды меню ----------
    def calc_k(self):
        self.ensure_loaded()
        df = self.current()
        qi = [c for c, v in self.vars.items() if v.get()]
        if not qi:
            return messagebox.showwarning("Внимание", "Выберите квази-идентификаторы")

        k = int(k_per_row(df, qi).min())
        need = required_k(len(df))
        name = "обезличенный" if self.anon is not None else "исходный"
        lines = [f"Датасет: {name}, строк: {len(df)}",
                 f"K = {k}, нужно >= {need}: {'приемлемо' if k >= need else 'НЕприемлемо'}",
                 "", "Топ плохих K (доля строк):"]
        for kv, cnt, pct in top_bad_k(df, qi):
            lines.append(f"  {kv} ({pct:.2f}%)  строк: {cnt}")

        uniq = unique_rows(df, qi)
        lines.append(f"\nУникальных строк (K=1): {len(uniq)}")
        if k == 1:
            lines.append(uniq[qi].head(50).to_string())
            if len(uniq) > 50:
                lines.append(f"... показаны первые 50 из {len(uniq)}")
        self.show("\n".join(lines))

    def run_anonymize(self):
        self.ensure_loaded()
        self.anon = anonymize(self.orig)
        self.build_checks(self.anon)
        self.show(f"Обезличено (k = {required_k(len(self.orig))} для агрегации и подавления).\n"
                  "Столбцы изменились, проверьте чекбоксы и нажмите «рассчитать k-anonymity».\n"
                  "Чтобы записать файл, нажмите «сохранить результат».")

    def utility(self):
        if self.anon is None:
            return messagebox.showwarning("Внимание", "Сначала обезличьте датасет")
        # приводим оригинал к тому же представлению, что и обезличенный набор
        cmp = generalize_quantity(generalize_datetime(self.orig.copy()))
        cmp = generalize_coords(cmp, COORD_DECIMALS)
        cols = ["price", "total", "lat", "lon", "quantity", "date", "time_of_day"]
        lines = ["KLD по столбцам (0 = распределение не изменилось):"]
        for c in cols:
            lines.append(f"  {c:12} {kld_column(cmp[c], self.anon[c]):.4f}")
        lines.append("\nСтатистика до / после:")
        lines.append(stats_compare(self.orig, self.anon).round(2).to_string())
        self.show("\n".join(lines))

    def save_to_disk(self):
        # относительное имя -> в папку с кодом; абсолютный путь (из «Обзор») остаётся как есть
        path = os.path.join(CODE_DIR, self.out_name.get())
        save_dataset(self.anon, path)
        return path

    def save(self):
        if self.anon is None:
            return messagebox.showwarning("Внимание", "Сначала обезличьте датасет")
        messagebox.showinfo("Готово", f"Сохранено: {self.save_to_disk()}")


if __name__ == "__main__":
    App().mainloop()
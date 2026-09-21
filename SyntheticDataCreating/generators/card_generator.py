import random

def luhn_checksum(number: str) -> int:
    """Считает контрольную цифру по алгоритму Луна."""
    digits = [int(d) for d in number]
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total = sum(digits)
    return (10 - total % 10) % 10


def generate_card(
    banks_list: list[str],
    banks_probability: list[float],
    BANKS: dict[int, dict], 
    CARD_LENGTH: dict[str, int]
) -> str:
    
    bank = random.choices(banks_list, weights=banks_probability, k=1)[0]

    for b in BANKS.values():
        if b["name"] == bank:
            bank = b
            break
    if bank is None:
        raise ValueError(f"Банк '{bank}' не найден")

    card = random.choice(bank["cards"])
    bin_code = random.choice(card["bins"])
    card_length = CARD_LENGTH[card["payment_system"]]

    random_digits_count = card_length - len(bin_code) - 1
    random_part = "".join(str(random.randint(0, 9)) for _ in range(random_digits_count))

    number_without_check = bin_code + random_part
    check_digit = luhn_checksum(number_without_check)

    full_number = number_without_check + str(check_digit)
    return full_number


class CardRegistry:
    def __init__(self, max_repeats: int = 5, reuse_probability: float = 0.3):
        self.max_repeats = max_repeats
        self.reuse_probability = reuse_probability
        self._usage: dict[str, int] = {}
 
    def _reusable_cards(self) -> list[str]:
        return [num for num, count in self._usage.items() if count < self.max_repeats]
 
    def get_card(self, banks_list, banks_probability, BANKS, CARD_LENGTH) -> str:
        reusable = self._reusable_cards()
        if reusable and random.random() < self.reuse_probability:
            card_number = random.choice(reusable)
            self._usage[card_number] += 1
            return card_number

        while True:
            new_card = generate_card(banks_list, banks_probability, BANKS, CARD_LENGTH)
            if new_card not in self._usage:
                self._usage[new_card] = 1
                return new_card


            
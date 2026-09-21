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


import random


def _generate_raw_number() -> str:
    return str(random.randint(1, 999_999))


class ReceiptRegistry:
    def __init__(self):
        self._used: dict[str, set[str]] = {}

    def generate_receipt_number(self, store_name: str) -> str:
        used_in_store = self._used.setdefault(store_name, set())

        while True:
            number = _generate_raw_number()
            if number not in used_in_store:
                used_in_store.add(number)
                return number
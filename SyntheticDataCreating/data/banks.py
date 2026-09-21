
#Справочник банков-эмитентов и платёжных систем для генерации номеров карт.

banks_list: list[str]  = ["Сбербанк", "ВТБ", "Газпромбанк", "Альфа-Банк", "Т-Банк", "Россельхозбанк", "Почта Банк", "Промсвязьбанк"]
banks_probability: list[float] = [43.51, 22.97, 11.49, 8.71, 3.66, 3.55, 0.32, 5.79]

CARD_LENGTH: dict[str, int] = {
    "MIR": 16,
    "VISA": 16,
    "MASTERCARD": 16,
    "UNIONPAY": 16,
}

BANKS: dict[int, dict] = {
    1: {
        "name": "Сбербанк",
        "cards": [
            {"payment_system": "MIR", "bins": ["220220", "220221", "220222"]},
            {"payment_system": "VISA", "bins": ["427600", "427601", "427602"]},
            {"payment_system": "MASTERCARD", "bins": ["546901", "546902"]},
        ],
    },
    2: {
        "name": "ВТБ",
        "cards": [
            {"payment_system": "MIR", "bins": ["220024", "220025"]},
            {"payment_system": "VISA", "bins": ["400119", "400120"]},
            {"payment_system": "MASTERCARD", "bins": ["518901", "518902"]},
        ],
    },
    3: {
        "name": "Газпромбанк",
        "cards": [
            {"payment_system": "MIR", "bins": ["220412", "220413"]},
            {"payment_system": "MASTERCARD", "bins": ["529389"]},
            {"payment_system": "UNIONPAY", "bins": ["622128"]},
        ],
    },
    4: {
        "name": "Альфа-Банк",
        "cards": [
            {"payment_system": "MIR", "bins": ["220305", "220306"]},
            {"payment_system": "VISA", "bins": ["415482", "415483"]},
            {"payment_system": "MASTERCARD", "bins": ["512890", "512891"]},
        ],
    },
    5: {
        "name": "Т-Банк",
        "cards": [
            {"payment_system": "MIR", "bins": ["220070", "220071"]},
            {"payment_system": "VISA", "bins": ["437772", "437773"]},
            {"payment_system": "MASTERCARD", "bins": ["521324", "521325"]},
        ],
    },
    6: {
        "name": "Россельхозбанк",
        "cards": [
            {"payment_system": "MIR", "bins": ["220130"]},
            {"payment_system": "UNIONPAY", "bins": ["622398"]},
        ],
    },
    7: {
        "name": "Почта Банк",
        "cards": [
            {"payment_system": "MIR", "bins": ["220456"]},
        ],
    },
    8: {
        "name": "Промсвязьбанк",
        "cards": [
            {"payment_system": "MIR", "bins": ["220367"]},
            {"payment_system": "UNIONPAY", "bins": ["622519"]},
        ],
    },
}
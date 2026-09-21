
#50 категорий x 10 брендов = 500 брендов.

categories: list[str] = [
    "Электроника",
    "Смартфоны",
    "Ноутбуки",
    "Бытовая техника",
    "ТВ и аудио",
    "Одежда женская",
    "Одежда мужская",
    "Обувь",
    "Детская одежда",
    "Спортивная одежда",
    "Косметика",
    "Парфюмерия",
    "Уход за волосами",
    "Уход за кожей",
    "Бытовая химия",
    "Продукты питания",
    "Напитки безалкогольные",
    "Алкоголь",
    "Кофе и чай",
    "Кондитерские изделия",
    "Мебель",
    "Товары для дома",
    "Строительные материалы",
    "Инструменты",
    "Автотовары",
    "Шины",
    "Автомобили",
    "Мотоциклы",
    "Велосипеды",
    "Детские товары (игрушки)",
    "Товары для животных",
    "Спортивные товары",
    "Часы",
    "Ювелирные изделия",
    "Сумки и аксессуары",
    "Канцтовары",
    "Книги и медиа",
    "Игры и консоли",
    "Фото и видео техника",
    "Климатическая техника",
    "Сантехника",
    "Освещение",
    "Текстиль для дома",
    "Постельное белье",
    "Посуда",
    "Кухонная техника",
    "Молочные продукты",
    "Пиво",
    "Табачные изделия",
    "Медицина и БАДы",
]

brand_groups: dict[str, list[str]] = {
    "Электроника": [
        "Apple", "Samsung", "Xiaomi", "Huawei", "Honor",
        "Sony", "LG", "Lenovo", "Asus", "Acer",
    ],
    "Смартфоны": [
        "Apple", "Samsung", "Xiaomi", "Realme", "Honor",
        "Tecno", "Infinix", "OnePlus", "Vivo", "Oppo",
    ],
    "Ноутбуки": [
        "Lenovo", "HP", "Dell", "Asus", "Acer",
        "MSI", "Apple", "Huawei", "Digma", "Irbis",
    ],
    "Бытовая техника": [
        "Bosch", "Samsung", "LG", "Haier", "Midea",
        "Indesit", "Beko", "Electrolux", "Hisense", "Gorenje",
    ],
    "ТВ и аудио": [
        "Samsung", "LG", "Sony", "Hisense", "TCL",
        "JBL", "Sonos", "Xiaomi", "Haier", "Harper",
    ],
    "Одежда женская": [
        "Zara", "H&M", "Mango", "Befree", "Zarina",
        "Love Republic", "Gloria Jeans", "InCity", "Sela", "O'stin",
    ],
    "Одежда мужская": [
        "Zara", "Massimo Dutti", "Uniqlo", "Tom Farr", "Sela",
        "O'stin", "Finn Flare", "Bosco", "Kanzler", "Antony Morato",
    ],
    "Обувь": [
        "Ecco", "Reebok", "Nike", "Adidas", "Puma",
        "Ralf Ringer", "Zenden", "Kari", "Respect", "Salamander",
    ],
    "Детская одежда": [
        "Gloria Jeans", "Acoola", "Choupette", "Orby", "Crockid",
        "Zara Kids", "Mothercare", "H&M Kids", "Sela Kids", "Finn Flare Kids",
    ],
    "Спортивная одежда": [
        "Nike", "Adidas", "Puma", "Reebok", "Under Armour",
        "Demix", "Outventure", "Kappa", "Fila", "New Balance",
    ],
    "Косметика": [
        "L'Oreal", "Maybelline", "Nivea", "Vichy", "La Roche-Posay",
        "Yves Rocher", "Faberlic", "Bell", "Eveline Cosmetics", "Belor Design",
    ],
    "Парфюмерия": [
        "Chanel", "Dior", "Lancome", "Hugo Boss", "Versace",
        "Carolina Herrera", "Nina Ricci", "Paco Rabanne", "Giorgio Armani", "Yves Saint Laurent",
    ],
    "Уход за волосами": [
        "Schwarzkopf", "Wella", "L'Oreal Professionnel", "Pantene", "Head & Shoulders",
        "Syoss", "Gliss Kur", "Estel", "Kapous", "Concept",
    ],
    "Уход за кожей": [
        "Nivea", "Garnier", "Vichy", "La Roche-Posay", "Bioderma",
        "Librederm", "Чистая Линия", "Natura Siberica", "Planeta Organica", "Green Mama",
    ],
    "Бытовая химия": [
        "Tide", "Ariel", "Persil", "Fairy", "Domestos",
        "Comet", "Mr Proper", "AOS", "Sarma", "BiMax",
    ],
    "Продукты питания": [
        "Nestle", "Mars", "Danone", "PepsiCo", "Cherkizovo",
        "Miratorg", "Chernogolovka", "Makfa", "Slavyanka", "Ostankino",
    ],
    "Напитки безалкогольные": [
        "Coca-Cola", "Pepsi", "Добрый", "Rich", "J7",
        "Сады Придонья", "Fanta", "Sprite", "Черноголовка", "Байкал",
    ],
    "Алкоголь": [
        "Балтика", "Beluga", "Русский Стандарт", "Столичная", "Зелёная Марка",
        "Очаково", "Бочкарёв", "Кристалл", "Nemiroff", "Хортица",
    ],
    "Кофе и чай": [
        "Nescafe", "Jacobs", "Jardin", "Egoiste", "Greenfield",
        "Ahmad Tea", "Lipton", "Curtis", "Tess", "Maxwell House",
    ],
    "Кондитерские изделия": [
        "Nestle", "Mars", "Ferrero", "Konti", "Slavyanka",
        "Красный Октябрь", "Бабаевский", "Алёнка", "Рот Фронт", "KDV",
    ],
    "Мебель": [
        "IKEA", "Hoff", "Шатура", "Divan.ru", "Askona",
        "Столплит", "Mebelvia", "Miass Mebel", "Пинскдрев", "Anrex",
    ],
    "Товары для дома": [
        "Tefal", "Zwilling", "IKEA", "Home Market", "Tescoma",
        "Vitesse", "Rondell", "Nadoba", "Fissman", "Bergner",
    ],
    "Строительные материалы": [
        "Knauf", "Ceresit", "Bosch", "Makita", "ТехноНИКОЛЬ",
        "Rockwool", "Baumit", "Волма", "Юнис", "Основит",
    ],
    "Инструменты": [
        "Bosch", "Makita", "DeWalt", "Metabo", "Интерскол",
        "Hitachi", "Зубр", "Sturm", "Kraft", "Hammer",
    ],
    "Автотовары": [
        "Bosch", "Castrol", "Mobil", "Shell", "Liqui Moly",
        "ZIC", "Лукойл", "K&N", "Filtron", "Champion",
    ],
    "Шины": [
        "Michelin", "Bridgestone", "Continental", "Pirelli", "Nokian",
        "Cordiant", "Кама", "Nordman", "Viatti", "Matador",
    ],
    "Автомобили": [
        "Lada", "Chery", "Haval", "Geely", "Changan",
        "Москвич", "EXEED", "Omoda", "GAC", "Voyah",
    ],
    "Мотоциклы": [
        "Honda", "Yamaha", "Suzuki", "Kawasaki", "Racer",
        "Irbis", "BMW Motorrad", "Zongshen", "Stels", "CFMoto",
    ],
    "Велосипеды": [
        "Stels", "Forward", "Merida", "Giant", "Trek",
        "Author", "Format", "Stinger", "Scott", "Cube",
    ],
    "Детские товары (игрушки)": [
        "Lego", "Hasbro", "Mattel", "Zvezda", "Stellar",
        "Simba", "Chicco", "Playmobil", "Bondibon", "Origami",
    ],
    "Товары для животных": [
        "Purina", "Royal Canin", "Pedigree", "Whiskas", "Perfect Fit",
        "Kitekat", "Chappi", "Sirius", "Monge", "Brit",
    ],
    "Спортивные товары": [
        "Nike", "Adidas", "Decathlon", "Puma", "Wilson",
        "Head", "Yonex", "Torneo", "Demix", "Reebok",
    ],
    "Часы": [
        "Casio", "Citizen", "Seiko", "Orient", "Fossil",
        "Слава", "Полёт", "Восток", "Diesel", "Tissot",
    ],
    "Ювелирные изделия": [
        "Sokolov", "Pandora", "Adamas", "Sunlight", "585 Золотой",
        "Kristall", "Бронницкий Ювелир", "Яшма Золото", "Золотой", "Diamant",
    ],
    "Сумки и аксессуары": [
        "Samsonite", "Guess", "Coccinelle", "Furla", "Wenger",
        "Zenden", "Solo", "Grifon", "Fabretti", "Lamark",
    ],
    "Канцтовары": [
        "Erich Krause", "Berlingo", "Attache", "Brauberg", "Staff",
        "Pilot", "Bic", "Faber-Castell", "Stabilo", "Kores",
    ],
    "Книги и медиа": [
        "Эксмо", "АСТ", "Просвещение", "Росмэн", "Азбука",
        "Альпина Паблишер", "МИФ", "Феникс", "Питер", "Рипол Классик",
    ],
    "Игры и консоли": [
        "PlayStation", "Nintendo", "Xbox", "Steam", "Logitech",
        "Razer", "HyperX", "Defender", "A4Tech", "SVEN",
    ],
    "Фото и видео техника": [
        "Canon", "Nikon", "Sony", "Fujifilm", "Panasonic",
        "GoPro", "DJI", "Olympus", "Sigma", "Tamron",
    ],
    "Климатическая техника": [
        "Ballu", "Electrolux", "Daikin", "Mitsubishi Electric", "Haier",
        "Midea", "Hisense", "Timberk", "Royal Clima", "Zanussi",
    ],
    "Сантехника": [
        "Grohe", "Hansgrohe", "Cersanit", "Roca", "Iddis",
        "Vitra", "Gustavsberg", "Sanita", "Damixa", "AM.PM",
    ],
    "Освещение": [
        "Philips", "Osram", "Camelion", "Navigator", "Era",
        "Feron", "Gauss", "Jazzway", "In Home", "Ledvance",
    ],
    "Текстиль для дома": [
        "Ecotex", "Togas", "Ivanovo Textile", "Arya", "Cleo",
        "Guten Morgen", "Kazanov", "Nordtex", "Wenge", "Valtery",
    ],
    "Постельное белье": [
        "Togas", "Ecotex", "Arya", "Cleo", "Guten Morgen",
        "Verossa", "Sofi De Marko", "4 Сезона", "Univers Textile", "Nordtex",
    ],
    "Посуда": [
        "Tefal", "Zwilling", "Rondell", "Vitesse", "Fissman",
        "Nadoba", "Кукмара", "Tescoma", "Bergner", "Vinzer",
    ],
    "Кухонная техника": [
        "Bosch", "Philips", "Redmond", "Polaris", "Kitfort",
        "Scarlett", "Tefal", "Moulinex", "Braun", "Xiaomi",
    ],
    "Молочные продукты": [
        "Простоквашино", "Домик в деревне", "Danone", "Valio", "Петмол",
        "Чудо", "Активиа", "Вологодское", "Bio Balance", "Экомилк",
    ],
    "Пиво": [
        "Балтика", "Жигулёвское", "Очаково", "Tinkoff", "Barrel",
        "Heineken", "Efes", "Amstel", "Невское", "Bavaria",
    ],
    "Табачные изделия": [
        "Marlboro", "Winston", "Camel", "Parliament", "LD",
        "Bond Street", "Rothmans", "Chapman", "Kent", "West",
    ],
    "Медицина и БАДы": [
        "Эвалар", "Solgar", "Doppelherz", "Витамир", "Фармак",
        "Sandoz", "Teva", "Berlin-Chemie", "Нижфарм", "Materia Medica",
    ],
}

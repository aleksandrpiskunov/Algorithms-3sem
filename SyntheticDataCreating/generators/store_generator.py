import datetime
import random
import re
from typing import Dict, List

TZ = datetime.timezone(datetime.timedelta(hours=3))
DAYS_BACK = 365 * 2
HOURS_RE = re.compile(r"(\d{1,2}):(\d{2})\s*[-–—]\s*(\d{1,2}):(\d{2})")


def generate_store(stores: Dict[int, dict]) -> str:
    if not stores:
        raise ValueError("stores is empty")
    return random.choice(list(stores.values()))["name"]


def generate_coords(stores: Dict[int, dict], store: str) -> List[float]:
    found = next((s for s in stores.values() if s["name"] == store), None)
    if found is None:
        raise ValueError(f"store {store!r} not found")
    points = found.get("points") or []
    if not points:
        raise ValueError(f"store {store!r} has no points")
    point = random.choice(points)
    return [point["lat"], point["lon"]]


def generate_datetime(stores: Dict[int, dict], store: str) -> str:
    found = next((s for s in stores.values() if s["name"] == store), None)
    if found is None:
        raise ValueError(f"store {store!r} not found")
    points = found.get("points") or []
    if not points:
        raise ValueError(f"store {store!r} has no points")
    point = random.choice(points)

    # часы работы выбранной точки
    text = (point.get("hours") or "").strip().lower()
    if not text or "круглосуточно" in text or "24/7" in text:
        open_min, duration = 0, 24 * 60
    else:
        m = HOURS_RE.search(text)
        if not m:
            raise ValueError(f"unsupported hours format: {point.get('hours')!r}")
        h1, m1, h2, m2 = map(int, m.groups())
        open_min = h1 * 60 + m1
        end = h2 * 60 + m2
        if end <= open_min:  # работа через полночь
            end += 24 * 60
        duration = end - open_min

    # время внутри часов работы, не из будущего
    now = datetime.datetime.now(TZ)
    day = now.date() - datetime.timedelta(days=random.randint(0, DAYS_BACK))
    minute = open_min + random.randrange(duration)
    ts = datetime.datetime.combine(day, datetime.time(0), tzinfo=TZ) + datetime.timedelta(minutes=minute)
    if ts > now:
        ts -= datetime.timedelta(days=1)
    return ts.isoformat()
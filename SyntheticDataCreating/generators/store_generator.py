import datetime
import random
from typing import Dict, List


def generate_store(stores: Dict[int, dict]) -> str:
    if not stores:
        raise ValueError("stores is empty")
    store = random.choice(list(stores.values()))
    return store["name"]


def generate_datetime(stores: Dict[int, dict]) -> str:
    now = datetime.datetime.now(tz=datetime.timezone.utc).astimezone()
    end = now
    start = now - datetime.timedelta(days=365 * 2)
    random_ts = start + (end - start) * random.random()

    tz = datetime.timezone(datetime.timedelta(hours=3))
    random_ts = random_ts.astimezone(tz)

    random_ts = random_ts.replace(second=0, microsecond=0)
    return random_ts.isoformat()


def generate_coords(stores: Dict[int, dict]) -> List[float]:
    if not stores:
        raise ValueError("stores is empty")
    store = random.choice(list(stores.values()))
    points = store.get("points") or []
    if not points:
        raise ValueError("store has no points")
    point = random.choice(points)
    return [point["lat"], point["lon"]]
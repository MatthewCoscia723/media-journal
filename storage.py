import json
import os
from models import Entry

DATA_FILE = os.path.join("data", "journal.json")


def load_entries() -> list[Entry]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Entry.from_dict(item) for item in raw]


def save_entries(entries: list[Entry]) -> None:
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in entries], f, indent=2)

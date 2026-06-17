from models import Entry
import storage


def add_entry(title: str, media_type: str, date: str, rating: int, notes: str = "", artist: str = "") -> Entry:
    entries = storage.load_entries()
    new_id = max((e.id for e in entries), default=0) + 1
    entry = Entry(title=title, media_type=media_type, date=date, rating=rating, id=new_id, notes=notes, artist=artist)
    entries.append(entry)
    storage.save_entries(entries)
    return entry


def search_entries(query: str) -> list[Entry]:
    entries = storage.load_entries()
    return [e for e in entries if query.lower() in e.title.lower()]


def list_entries(media_type: str = None) -> list[Entry]:
    entries = storage.load_entries()
    if media_type:
        entries = [e for e in entries if e.media_type.lower() == media_type.lower()]
    return entries


def delete_entry(entry_id: int) -> bool:
    entries = storage.load_entries()
    filtered = [e for e in entries if e.id != entry_id]
    if len(filtered) == len(entries):
        return False  # nothing was removed
    storage.save_entries(filtered)
    return True

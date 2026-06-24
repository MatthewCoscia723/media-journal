from models import Entry
import storage
import random

def add_entry(title: str, media_type: str, date: str, rating: int, notes: str = "", artist: str = "", favorite=False, status: str = "") -> Entry:
    entries = storage.load_entries()

    if any(title.lower() == e.title.lower() for e in entries):
        inp = input(f"Warning: '{title}' already exists. Add anyway? (y/n): ").strip().lower()
        if inp != "y":
            return None

    new_id = max((e.id for e in entries), default=0) + 1
    entry = Entry(title=title, media_type=media_type, date=date, rating=rating, id=new_id, notes=notes, artist=artist, favorite=favorite, status=status)
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

def edit_entry(entry_id: int) -> bool:
    entries = storage.load_entries()
    for e in entries:
        if e.id == entry_id:
            print(f"Editing Entry #{e.id}: {e.title}")
            while True:
                new_rating = input(f"New rating (1-10, current: {e.rating}, press Enter to skip): ").strip()
                if new_rating == "":
                    break
                if new_rating.isdigit() and 1 <= int(new_rating) <= 10:
                    e.rating = int(new_rating)
                    print("Entry updated")
                    break
                print("  Please enter a number between 1 and 10")
            new_notes = input(f"New notes (current: {e.notes}): ").strip()
            if new_notes:
                e.notes = new_notes
                print("Entry updated")
            while True:
                new_favorite = input(f"Mark as favorite (y/n, current: {'y' if e.favorite else 'n'}, press Enter to skip): ").strip().lower()
                if new_favorite == "":
                    break
                if new_favorite in ("y", "n"):
                    e.favorite = (new_favorite == "y")
                    print("Entry updated")
                    break
                print("Please enter either 'y' or 'n'")
            while True:
                new_status = input(f"New completion status ('completed', 'in progress', 'dropped', or 'planned', currently: {e.status}, press Enter to skip): ").strip().lower()
                if new_status == "":
                    break
                if new_status in ("completed", "in progress", "dropped", "planned"):
                    e.status = new_status
                    print("Entry updated")
                    break
                print("Please enter either 'completed', 'in progress', 'dropped', or 'planned'")
            storage.save_entries(entries)
            return True
    return False  # entry not found

def list_favorites() -> list[Entry]:
    entries = storage.load_entries()
    return [e for e in entries if e.favorite]

def get_stats() -> dict:
    entries = storage.load_entries()
    if not entries:
        return {}
    average = 0
    for e in entries:
        average += e.rating
    average /= len(entries)
    movie = 0
    tv = 0
    game = 0
    song = 0
    album = 0
    for e in entries:
        if e.media_type == "movie":
            movie += 1
        if e.media_type == "tv":
            tv += 1
        if e.media_type == "game":
            game += 1
        if e.media_type == "song":
            song += 1
        if e.media_type == "album":
            album += 1
    return {
        "total" : len(entries), 
        "average" : average, 
        "movie" : movie, 
        "tv" : tv, 
        "game" : game, 
        "song" : song, 
        "album" : album
    }

def get_recent(n = 5) -> list[Entry]:
    entries = storage.load_entries()
    return [e for e in entries[-n:]]

def random_entry():
    entries = storage.load_entries()
    # what i was going to do was to have it pick a random id and then id find the entry that matched
    # up to it and then return that, but intstead Claude showed me this
    return random.choice(entries)
import journal
import export

VALID_TYPES = ("movie", "tv", "game", "song", "album")

TYPE_LABELS = {
    "movie": "movie",
    "tv": "TV show",
    "game": "game",
    "song": "song",
    "album": "album"
}

def print_entries(entries):
    if not entries:
        print("  No entries found.")
        return
    header = f"{'ID':<4} {'Type':<7} {'Rating':<7} {'Date':<12} {'Title':<30} {'Artist':<20} Notes"
    print("\n" + header)
    print("-" * len(header))
    for e in entries:
        print(f"{e.id:<4} {e.media_type:<7} {e.rating:<7} {e.date:<12} {e.title:<30} {e.artist:<20} {e.notes}")
    print()


def prompt_media_type():
    while True:
        t = input("  Type (movie / tv / game / song / album): ").strip().lower()
        if t in VALID_TYPES:
            return t
        print("  Please enter: movie, tv, game, song, or album")


def prompt_rating():
    while True:
        raw = input("  Rating (1–10): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= 10:
            return int(raw)
        print("  Please enter a number between 1 and 10.")


def prompt_date():
    while True:
        d = input("  Date watched/played/listened (YYYY-MM-DD): ").strip()
        parts = d.split("-")
        if len(parts) == 3 and all(p.isdigit() for p in parts) and len(parts[0]) == 4:
            return d
        print("  Please use the format YYYY-MM-DD, e.g. 2024-06-15")


def do_add():
    print("\n-- Add Entry --")
    title = input("  Title: ").strip()
    media_type = prompt_media_type()
    artist = ""
    if media_type in ("song", "album"):
        artist = input("  Artist: ").strip()
    date = prompt_date()
    rating = prompt_rating()
    notes = input("  Notes (optional, press Enter to skip): ").strip()
    favorite = input("Mark as favorite (y/n): ").strip().lower() == "y"
    entry = journal.add_entry(title, media_type, date, rating, notes, artist, favorite)
    print(f"\n  Saved! Entry #{entry.id}: {entry.title}")


def do_view_all():
    print("\n-- All Entries --")
    print_entries(journal.list_entries())


def do_view_by_type():
    media_type = prompt_media_type()
    print(f"\n-- {media_type.title()} Entries --")
    print_entries(journal.list_entries(media_type=media_type))


def do_delete():
    print("\n-- Delete Entry --")
    raw = input("  Enter the ID to delete: ").strip()
    if not raw.isdigit():
        print("  Invalid ID.")
        return
    removed = journal.delete_entry(int(raw))
    print("  Entry deleted." if removed else "  No entry found with that ID.")


def do_search():
    print("\n-- Search by Title --")
    query = input("  Enter search term: ").strip()
    results = journal.search_entries(query)
    print(f"\n-- Results for '{query}' --")
    print_entries(results)

def do_edit():
    print("\n-- Edit Entry --")
    id_of_change = input("Enter the ID of the item you want to edit: ").strip()
    if not id_of_change.isdigit():
        print("  Invalid ID.")
        return
    success = journal.edit_entry(int(id_of_change))
    if not success:
        print("  No entry found with that ID.")

def do_favorites():
    print("\n-- Favorite Entries --")
    print_entries(journal.list_favorites())

def do_stats():
    print("===== My Stats =====")
    stats = journal.get_stats()
    print(f"Total entries: {stats['total']}")
    print(f"Average rating: {stats['average']:.1f}")
    print("By type:")
    print(f"movie : {stats['movie']} entries")
    print(f"tv : {stats['tv']} entries")
    print(f"game : {stats['game']} entries")
    print(f"song: {stats['song']} entries")
    print(f"album: {stats['album']} entries")

def do_export():
    export.export_to_txt()
    print("Journal successfully exported to 'media_journal.txt'!")

def do_recent():
    print("\n-- Recent Entries --")
    print_entries(journal.get_recent())

def do_random():
    print("Your random piece of media from your journal is: ")
    entry = journal.random_entry()
    label = TYPE_LABELS[entry.media_type]
    artist_part = f" by {entry.artist}" if entry.media_type in ("song", "album") else ""
    print(f"The {label} {entry.title}{artist_part} with a rating of {entry.rating}/10")

MENU = """
===== Media Journal =====
1. Add entry
2. View all entries
3. View by type
4. Delete entry
5. Search by title
6. Edit entry
7. View favorites
8. View stats
9. Export journal
10. View recent entries
11. Pick random media piece
12. Quit
"""

ACTIONS = {
    "1": do_add,
    "2": do_view_all,
    "3": do_view_by_type,
    "4": do_delete,
    "5": do_search,
    "6": do_edit,
    "7": do_favorites,
    "8": do_stats,
    "9": do_export,
    "10": do_recent,
    "11": do_random

}


def main():
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "12":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("  Invalid choice. Please enter 1–12.")


if __name__ == "__main__":
    main()

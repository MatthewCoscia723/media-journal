import journal

VALID_TYPES = ("movie", "tv", "game", "song", "album")


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
    entry = journal.add_entry(title, media_type, date, rating, notes, artist)
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


MENU = """
===== Media Journal =====
1. Add entry
2. View all entries
3. View by type
4. Delete entry
5. Search by title
6. Quit
"""

ACTIONS = {
    "1": do_add,
    "2": do_view_all,
    "3": do_view_by_type,
    "4": do_delete,
    "5": do_search,
}


def main():
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("  Invalid choice. Please enter 1–6.")


if __name__ == "__main__":
    main()

import journal
import export
from tabulate import tabulate
from colorama import init, Fore, Style
init()

VALID_TYPES = ("movie", "tv", "game", "song", "album")

TYPE_LABELS = {
    "movie": "movie",
    "tv": "TV show",
    "game": "game",
    "song": "song",
    "album": "album"
}

def color_row(e):
    if e.favorite:
        return [Fore.YELLOW + str(e.id) + Style.RESET_ALL,
                Fore.YELLOW + e.media_type + Style.RESET_ALL,
                Fore.YELLOW + str(e.rating) + Style.RESET_ALL,
                Fore.YELLOW + e.date + Style.RESET_ALL,
                Fore.YELLOW + e.title + Style.RESET_ALL,
                Fore.YELLOW + e.artist + Style.RESET_ALL,
                Fore.YELLOW + e.notes + Style.RESET_ALL]
    return [e.id, e.media_type, e.rating, e.date, e.title, e.artist, e.notes]

def print_entries(entries):
    if not entries:
        print("  No entries found.")
        return
    headers = [Fore.MAGENTA + col + Style.RESET_ALL for col in ["ID", "Type", "Rating", "Date", "Title", "Artist", "Notes"]]
    rows = [color_row(e) for e in entries]
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))


def prompt_media_type():
    while True:
        t = input("Type (movie / tv / game / song / album): ").strip().lower()
        if t in VALID_TYPES:
            return t
        print(Fore.RED + "Please enter: movie, tv, game, song, or album" + Style.RESET_ALL)


def prompt_rating():
    while True:
        raw = input("Rating (1–10): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= 10:
            return int(raw)
        print(Fore.RED + "Please enter a number between 1 and 10." + Style.RESET_ALL)


def prompt_date():
    while True:
        d = input("Date watched/played/listened (YYYY-MM-DD): ").strip()
        parts = d.split("-")
        if len(parts) == 3 and all(p.isdigit() for p in parts) and len(parts[0]) == 4:
            return d
        print(Fore.RED + "Please use the format YYYY-MM-DD, e.g. 2024-06-15" + Style.RESET_ALL)


def do_add():
    print(Fore.BLUE + "\n-- Add Entry --" + Style.RESET_ALL)
    title = input("Title: ").strip()
    media_type = prompt_media_type()
    artist = ""
    if media_type in ("song", "album"):
        artist = input("Artist: ").strip()
    date = prompt_date()
    rating = prompt_rating()
    notes = input("Notes (optional, press Enter to skip): ").strip()
    favorite = input("Mark as favorite (y/n): ").strip().lower() == "y"
    entry = journal.add_entry(title, media_type, date, rating, notes, artist, favorite)
    print(Fore.GREEN + f"\nSaved! Entry #{entry.id}: {entry.title}" + Style.RESET_ALL)


def do_view_all():
    print(Fore.BLUE + "\n-- All Entries --" + Style.RESET_ALL)
    print_entries(journal.list_entries())


def do_view_by_type():
    media_type = prompt_media_type()
    print(Fore.BLUE + f"\n-- {media_type.title()} Entries --" + Style.RESET_ALL)
    print_entries(journal.list_entries(media_type=media_type))


def do_delete():
    print(Fore.BLUE + "\n-- Delete Entry --" + Style.RESET_ALL)
    raw = input("  Enter the ID to delete: ").strip()
    if not raw.isdigit():
        print(Fore.RED + "  Invalid ID." + Style.RESET_ALL)
        return
    removed = journal.delete_entry(int(raw))
    if removed:
        print(Fore.GREEN + "Entry deleted." + Style.RESET_ALL)
    else:
        print(Fore.RED + "  No entry found with that ID." + Style.RESET_ALL)


def do_search():
    print(Fore.BLUE + "\n-- Search by Title --" + Style.RESET_ALL)
    query = input("  Enter search term: ").strip()
    results = journal.search_entries(query)
    print(Fore.BLUE + f"\n-- Results for '{query}' --" + Style.RESET_ALL)
    print_entries(results)

def do_edit():
    print(Fore.BLUE + "\n-- Edit Entry --" + Style.RESET_ALL)
    id_of_change = input("Enter the ID of the item you want to edit: ").strip()
    if not id_of_change.isdigit():
        print(Fore.RED + "Invalid ID." + Style.RESET_ALL)
        return
    success = journal.edit_entry(int(id_of_change))
    if not success:
        print(Fore.RED + "No entry found with that ID." + Style.RESET_ALL)

def do_favorites():
    print(Fore.BLUE + "\n-- Favorite Entries --" + Style.RESET_ALL)
    print_entries(journal.list_favorites())

def do_stats():
    print(Fore.BLUE + "===== My Stats =====" + Style.RESET_ALL)
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
    print(Fore.GREEN + "Journal successfully exported to 'media_journal.txt'!" + Style.RESET_ALL)

def do_recent():
    print(Fore.BLUE + "\n-- Recent Entries --" + Style.RESET_ALL)
    print_entries(journal.get_recent())

def do_random():
    print(Fore.BLUE + "Your random piece of media from your journal is: " + Style.RESET_ALL)
    entry = journal.random_entry()
    label = TYPE_LABELS[entry.media_type]
    artist_part = f" by {entry.artist}" if entry.media_type in ("song", "album") else ""
    print(f"The {label} {entry.title}{artist_part} with a rating of {entry.rating}/10")

MENU = Fore.CYAN + """
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
""" + Style.RESET_ALL

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
            print(Style.BRIGHT + Fore.BLUE + "Goodbye!" + Style.RESET_ALL)
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print(Fore.RED + "Invalid choice. Please enter 1–12." + Style.RESET_ALL)


if __name__ == "__main__":
    main()

import storage
from datetime import date

def export_to_txt():
    txt = open("media_journal.txt", "w+")
    entries = storage.load_entries()
    txt.write("================\n")
    txt.write("MY MEDIA JOURNAL\n")
    txt.write("================\n")
    txt.write(f"Exported on: {date.today()}\n\n")
    for e in entries:
        txt.write(f"ID: {e.id}\n")
        txt.write(f"Title: {e.title}\n")
        txt.write(f"Type: {e.media_type}\n")
        if e.media_type == "song" or e.media_type == "album":
            txt.write(f"Artist: {e.artist}\n") 
        txt.write(f"Date: {e.date}\n")
        txt.write(f"Rating: {e.rating}/10\n")
        txt.write(f"Notes: {e.notes}\n")
        txt.write(f"Favorite: {'Yes' if e.favorite == True else 'No'}\n\n")
    txt.close()

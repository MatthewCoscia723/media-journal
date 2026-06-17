from dataclasses import dataclass, field


@dataclass
class Entry:
    title: str
    media_type: str  # "movie", "tv", "game", "song", or "album"
    date: str        # ISO format: YYYY-MM-DD
    rating: int      # 1–10
    id: int = 0
    notes: str = ""
    artist: str = ""  # used for song and album entries
    favorite: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "media_type": self.media_type,
            "date": self.date,
            "rating": self.rating,
            "notes": self.notes,
            "artist": self.artist,
            "favorite": self.favorite,
        }

    @staticmethod
    def from_dict(data: dict) -> "Entry":
        return Entry(
            id=data["id"],
            title=data["title"],
            media_type=data["media_type"],
            date=data["date"],
            rating=data["rating"],
            notes=data.get("notes", ""),
            artist=data.get("artist", ""),
            favorite=data.get("favorite", False),
        )
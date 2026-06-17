from dataclasses import dataclass, field


@dataclass
class Entry:
    title: str
    media_type: str  # "movie", "tv", or "game"
    date: str        # ISO format: YYYY-MM-DD
    rating: int      # 1–10
    id: int = 0
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "media_type": self.media_type,
            "date": self.date,
            "rating": self.rating,
            "notes": self.notes,
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
        )

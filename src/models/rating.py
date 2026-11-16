from dataclasses import dataclass, field
from datetime import date
from .media import Media

@dataclass
class Rating:
    media: Media
    score: int
    rating_date: date = field(default_factory=date.today)

    def __post_init__(self):
        if not 1 <= self.score <= 5:
            raise ValueError("La puntuación debe estar entre 1 y 5")

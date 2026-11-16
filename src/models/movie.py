from dataclasses import dataclass
from .media import Media


@dataclass
class Movie(Media):
    duration_minutes: int = 0
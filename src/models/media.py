from abc import ABC
from dataclasses import dataclass, field

from .genre import Genre


@dataclass
class Media(ABC):
    id: int
    title: str
    description: str
    release_year: int
    genres: set[Genre] = field(default_factory=set)
    popularity: float = 0.0

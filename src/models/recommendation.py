from dataclasses import dataclass
from .media import Media

@dataclass
class Recommendation:
    media: Media
    similarity_score: float
    reason: str

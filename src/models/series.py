from dataclasses import dataclass
from .media import Media
from .series_status import SeriesStatus

@dataclass
class Series(Media):
    number_of_seasons: int = 0
    status: SeriesStatus = SeriesStatus.ONGOING
    
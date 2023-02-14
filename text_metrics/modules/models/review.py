from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    title: str
    content: str
    date: datetime

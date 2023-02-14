from dataclasses import dataclass

from textmetrics.modules.enums.polarity import Polarity


@dataclass
class LabelData:
    content: str
    polarity: Polarity

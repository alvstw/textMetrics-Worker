from dataclasses import dataclass

from text_metrics.modules.enums.polarity import Polarity


@dataclass
class LabelData:
    content: str
    polarity: Polarity

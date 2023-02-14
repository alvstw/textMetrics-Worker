from dataclasses import dataclass

from text_metrics.modules.models.review import Review


@dataclass
class AmazonReview(Review):
    amazon_comment_id: str

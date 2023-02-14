from dataclasses import dataclass

from textmetrics.modules.models.review import Review


@dataclass
class AmazonReview(Review):
    amazon_comment_id: str

from text_metrics.amazon_reviews_crawler import AmazonReviewsCrawler
from text_metrics.modules.models.amazon_review import AmazonReview


def get_amazon_reviews():
    reviews: list[AmazonReview] = []

    firefox_crawler = AmazonReviewsCrawler()

    firefox_crawler.start_crawler()
    reviews.extend(firefox_crawler.extract())

    while firefox_crawler.has_next_page() and len(reviews) < 100:
        firefox_crawler.next_page()
        reviews.extend(firefox_crawler.extract())

    for review in reviews:
        print(review)

    # Close the browser
    firefox_crawler.driver.quit()

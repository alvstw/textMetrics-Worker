from loguru import logger

from text_metrics.amazon_reviews_crawler import AmazonReviewsCrawler
from text_metrics.modules.helpers.server.product_api import post_amazon_product, post_product_price


class Fetcher:
    firefox_crawler: AmazonReviewsCrawler

    def __init__(self):
        self.firefox_crawler = AmazonReviewsCrawler()

    # noinspection PyBroadException
    def search(self, keyword: str, job_id: int = None):
        for n in range(10):
            try:
                self.firefox_crawler.search(keyword)
            except:
                self.firefox_crawler.continue_on_blocked()
                self.firefox_crawler.search(keyword)
                pass

            try:
                self.firefox_crawler.go_to_n_product_page(n)
                self.firefox_crawler.get_product_id()
            except:
                logger.info("Product page not found, skipping")
                continue

            asin = self.firefox_crawler.get_product_id()
            product_name = self.firefox_crawler.get_product_name()
            description = self.firefox_crawler.get_product_description()
            url = self.firefox_crawler.get_current_url()
            images = self.firefox_crawler.get_product_images()
            price = self.firefox_crawler.get_product_price()
            product_response = post_amazon_product(asin, product_name, description, url, images, job_id=job_id)
            if product_response.succeeded and price is not None:
                post_product_price(product_response.data.id, price)

        self.firefox_crawler.close()

import random
import re
from datetime import datetime
from time import sleep
from typing import Optional

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from text_metrics.modules.helpers.string_helper import encode_url
from text_metrics.modules.models.amazon_review import AmazonReview


# noinspection PyBroadException
class AmazonReviewsCrawler:
    driver: WebDriver

    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_product_id(self) -> str:
        result = re.match(r'https://www\.amazon\.com/[\w\W]*/dp/(\w+)/[\w\W]*', self.driver.current_url)
        if result is None:
            raise Exception("Product ID not found")
        return result.group(1)

    def get_product_name(self) -> str:
        product_name = self.driver.find_element(By.ID, "productTitle").text
        return product_name

    def get_current_url(self) -> str:
        return self.driver.current_url

    def search(self, query: str):
        logger.info("Searching for " + query)

        # Encode the query
        query = encode_url(query)

        # Navigate to the product page on Amazon
        product_url = f'https://www.amazon.com/s?k={query}'
        self.driver.get(product_url)

        # Check if the page is blocked by Amazon
        if self.check_is_blocked():
            raise Exception("Amazon blocked the request")

        # Wait for the page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )

    def check_is_blocked(self):
        # Check if the page is blocked by Amazon
        elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href='/ref=cs_503_link']")
        if len(elements) > 0:
            return True
        return False

    def continue_on_blocked(self):
        # Check if the page is blocked by Amazon
        elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href='/ref=cs_503_link']")
        if len(elements) > 0:
            # Click on the button to continue
            elements[0].click()

    # noinspection PyBroadException
    def go_to_n_product_page(self, n: int):
        logger.info(f"Going to {str(n)} product page ")

        try:
            # List View
            product_element = self.driver.find_elements(By.XPATH,
                                                        "//span[@class='a-size-medium a-color-base a-text-normal']")[n]
            product_element.click()
            return
        except:
            pass

        try:
            # Grid View
            product_element = self.driver.find_elements(By.XPATH,
                                                        "//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-3']")[
                n]
            product_element.click()
            return
        except:
            pass

        raise Exception("Could not find product element")

    def go_to_product_page(self, product_url: str):
        self.driver.get(product_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dp"))
        )

    # noinspection PyBroadException
    def get_product_description(self):
        try:
            return self.driver.find_element(By.ID, "productDescription").text
        except:
            pass

        try:
            return self.driver.find_element(By.XPATH, "//div[@class='feature_BulletPoints celwidget']").text
        except:
            pass

        try:
            return self.driver.find_element(By.XPATH, "//ul[@class='a-unordered-list a-vertical a-spacing-mini']").text
        except:
            pass

        return None

    def get_product_images(self):
        image_urls: list[str] = []
        try:
            image_url = self.driver.find_element(By.ID, "landingImage").get_attribute("src")
            image_urls.append(image_url)

            # while True:
            #     image_url = self.driver \
            #         .find_element(By.XPATH, f"(//img[@class='a-dynamic-image'])[{i}]") \
            #         .get_attribute("src")
            #     image_urls.append(image_url)
        except:
            pass

        return image_urls

    def get_product_price(self) -> Optional[float]:
        try:
            selector = "span[class='a-price a-text-price a-size-medium apexPriceToPay'] span[aria-hidden='true']"
            price = self.driver.find_element(By.CSS_SELECTOR, selector).text

            price = price.replace("$", "")
            price = price.replace(",", "")
            return float(price)
        except:
            pass

        return None

    def go_to_comment_page(self, comment_id: str):
        self.driver.find_element(By.LINK_TEXT, "See all reviews").click()

    def next_page(self):
        # Click the next page button
        next_page_button = self.driver.find_element(By.CSS_SELECTOR, "li.a-last a")
        next_page_button.click()

        # Wait for the reviews to load
        random_wait = random.Random().randint(1, 3)
        sleep(random_wait)

        # Make sure the reviews are loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "cm_cr-review_list"))
        )

    def has_next_page(self) -> bool:
        next_page_button = self.driver.find_elements(By.CSS_SELECTOR, "li.a-last a")
        return len(next_page_button) > 0

    def extract(self) -> list[AmazonReview]:
        reviews: list[AmazonReview] = []

        # Wait for the reviews to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "cm_cr-review_list"))
        )

        # Find a list of elements with id "customer_review-*"
        review_elements = self.driver.find_elements(By.CSS_SELECTOR, "[id^='customer_review-']")

        logger.info("Number of reviews: " + str(len(review_elements)))

        # Extract the information you need from the reviews
        for review_element in review_elements:
            amazon_id = review_element.get_attribute("id")
            title = review_element.find_element(By.CSS_SELECTOR, "a.a-size-base.review-title.a-text-bold").text
            author = review_element.find_element(By.CSS_SELECTOR, "span.a-profile-name").text
            rating = review_element.find_element(By.CSS_SELECTOR, "i.a-icon-star").text
            date = review_element.find_element(By.CSS_SELECTOR, "span.review-date").text
            content = review_element.find_element(By.CSS_SELECTOR, "span.a-size-base.review-text").text

            # Convert the date string to a datetime object
            date = date.split("on ")[1]
            parsed_date = datetime.strptime(date, "%B %d, %Y")

            review = AmazonReview(title=title, content=content, date=parsed_date, amazon_comment_id=amazon_id)
            review.amazon_comment_id = amazon_id
            review.title = title
            review.content = content

            reviews.append(review)

        return reviews

    def close(self):
        self.driver.close()

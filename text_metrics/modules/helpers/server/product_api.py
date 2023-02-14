import requests

from text_metrics.modules.helpers.server import api_base_url, handle_response
from text_metrics.modules.helpers.string_helper import encode_url
from text_metrics.modules.models.product import Product
from text_metrics.modules.models.utilities.server_response import ServerResponse


def post_amazon_product(asin: str, name: str, description: str, url: str, images: list[str], job_id: int = None) -> \
        ServerResponse[Product]:
    name = encode_url(name)
    description = encode_url(description)
    url = encode_url(url)

    url = f'{api_base_url}/Products/type=amazon?type=Amazon&asin={asin}&name={name}&description={description}&url={url}'
    for image in images:
        image = encode_url(image)
        url += f'&images={image}'
    if job_id is not None:
        url += f'&jobId={job_id}'

    response = requests.post(url)
    return handle_response(response)


def post_product_price(product_id: int, price: float, currency: str = 'USD'):
    url = f'{api_base_url}/Products/{product_id}/Price?price={price}'
    if currency is not None:
        url += f'&currency={currency}'

    response = requests.post(url)
    return handle_response(response)

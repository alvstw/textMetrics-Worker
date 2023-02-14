import urllib.parse


def encode_url(text: str):
    return urllib.parse.quote(text)

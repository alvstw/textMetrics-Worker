import re


def preprocess_string(string):
    # Remove all non-word characters (everything except numbers and letters)
    string = re.sub(r"[^\w\s]", '', string)
    # Replace all runs of whitespaces with no space
    string = re.sub(r"\s+", '', string)
    # replace digits with no space
    string = re.sub(r"\d", '', string)

    return string

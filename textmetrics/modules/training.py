import random

from textmetrics.modules.enums.general import DatasetType
from textmetrics.modules.extractors.amazon_review_polarity import extract_amazon_review_polarity_csv
from textmetrics.modules.extractors.twitter_data_1 import extract_twitter_data_1
from textmetrics.modules.extractors.twitter_data_2 import extract_twitter_data_2
from textmetrics.modules.models.label_data import LabelData
from textmetrics.modules.trainers.bert import train_bret


class Training:
    @staticmethod
    def get_training_data():
        data: list[LabelData] = []

        print('Extracting Amazon Review Polarity CSV...')
        data.extend(extract_amazon_review_polarity_csv())

        print('Extracting Twitter Data 1...')
        data.extend(extract_twitter_data_1())

        print('Extracting Twitter Data 2...')
        data.extend(extract_twitter_data_2())

        print('Shuffling data...')
        random.shuffle(data)

        return data

    @staticmethod
    def get_test_data():
        data: list[LabelData] = []

        print('Extracting Amazon Review Polarity CSV...')
        data.extend(extract_amazon_review_polarity_csv(dataset_type=DatasetType.TEST))

        print('Extracting Twitter Data 1...')
        data.extend(extract_twitter_data_1(dataset_type=DatasetType.TEST))

        print('Shuffling data...')
        random.shuffle(data)

        return data

    @staticmethod
    def train(data: list[LabelData]):
        print(f'Training on {len(data)} items...')

        texts = [label_data.content for label_data in data]
        labels = [label_data.polarity.value for label_data in data]

        train_bret(texts=texts, labels=labels)

        print('Training complete!')
        pass

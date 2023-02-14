import pandas as pd

from textmetrics.modules.enums.general import DatasetType
from textmetrics.modules.models.label_data import LabelData, Polarity


def extract_amazon_review_polarity_csv(dataset_type: DatasetType = DatasetType.TRAIN) -> list[LabelData]:
    # extract the data from the csv file using pandas
    file = 'datasets/amazon_review_polarity_csv/train.csv' if dataset_type == DatasetType.TRAIN else 'datasets/amazon_review_polarity_csv/test.csv'
    df = pd.read_csv(file, header=None)
    labels = df[0]
    texts = df[2]

    # create a list of LabelData objects
    label_data_list: list[LabelData] = []
    for i in range(len(labels)):
        polarity: Polarity = Polarity.POSITIVE if labels[i] == 2 else Polarity.NEGATIVE
        label_data_list.append(LabelData(polarity=polarity, content=texts[i]))

    return label_data_list

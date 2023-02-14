import pandas as pd

from text_metrics.modules.enums.general import DatasetType
from text_metrics.modules.models.label_data import LabelData, Polarity


def extract_twitter_data_1(dataset_type: DatasetType = DatasetType.TRAIN):
    # extract the data from the csv file using pandas
    file = 'datasets/twitter_data_1/train.csv' if dataset_type == DatasetType.TRAIN else 'datasets/twitter_data_1/test.csv'
    df = pd.read_csv(file, header=None)
    labels = df[2]
    texts = df[3]
    # create a list of LabelData objects
    label_data_list: list[LabelData] = []
    for i in range(len(labels)):
        if str(labels[i]).lower() == 'neutral':
            polarity: Polarity = Polarity.NEUTRAL
        elif str(labels[i]).lower() == 'positive':
            polarity: Polarity = Polarity.POSITIVE
        elif str(labels[i]).lower() == 'negative':
            polarity: Polarity = Polarity.NEGATIVE
        else:
            continue
        if str(texts[i]) == 'nan':
            continue
        label_data_list.append(LabelData(polarity=polarity, content=texts[i]))
    return label_data_list

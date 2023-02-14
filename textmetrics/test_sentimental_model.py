from tqdm import tqdm

from textmetrics.modules.analyzers.sentimental_analysis import SentimentalAnalysis
from textmetrics.modules.enums.polarity import Polarity
from textmetrics.modules.training import Training

analyzer = SentimentalAnalysis()

training = Training()
data = training.get_test_data()
print(f'Testing on {len(data)} items...')

# skip data that is neutral
data = [label_data for label_data in data if label_data.polarity != Polarity.NEUTRAL]
print(f'Filtered to {len(data)} items...')

# get texts and labels from the data
texts = [label_data.content for label_data in data]
labels = [label_data.polarity.value for label_data in data]

with tqdm(range(len(texts)), unit="texts") as pbar:
    accurate = 0
    for i in pbar:
        # get the predicted polarity
        predicted_polarity = analyzer.analyze(texts[i])
        # check if the predicted polarity matches the actual polarity
        if predicted_polarity == labels[i]:
            accurate += 1
        pbar.set_description(f"Accuracy: {accurate / (i + 1):.2%}")

print(f'Accuracy: {(accurate / len(texts)):.2%}')

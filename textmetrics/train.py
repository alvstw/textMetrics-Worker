from textmetrics.modules.models.label_data import Polarity
from textmetrics.modules.training import Training

training = Training()
data = training.get_training_data()
print(f'Got {len(data)} items for training...')

# skip data that is neutral
data = [label_data for label_data in data if label_data.polarity != Polarity.NEUTRAL]
print(f'Filtered to {len(data)} items for training...')

data = data[:10000]
training.train(data)

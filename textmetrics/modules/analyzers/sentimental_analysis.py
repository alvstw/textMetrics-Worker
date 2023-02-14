import torch
from transformers import BertTokenizer, BertForSequenceClassification

from textmetrics.modules.models.label_data import Polarity


class SentimentalAnalysis:
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    # device = torch.device("cpu")
    tokenizer: BertTokenizer
    model: BertForSequenceClassification

    def __init__(self):
        self.load_model()

    def load_model(self):
        device = self.device
        print(f"Using device: {device}")

        # Load the tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        # Load the model
        model = BertForSequenceClassification.from_pretrained('./machine_models/bert', num_labels=2)
        model.to(device)
        model.eval()

        self.tokenizer = tokenizer
        self.model = model


    def analyze(self, text) -> Polarity | None:
        # Define the new text samples
        new_texts = [text]

        # Encode the text samples
        input_ids = self.tokenizer.batch_encode_plus(new_texts, padding='max_length', return_tensors='pt')['input_ids']
        if input_ids.shape[1] > 512:
            return None

        # Move the input to the device
        input_ids = input_ids.to(self.device)
        input_ids.to(self.device)

        # Predict the sentiment of the new text samples
        with torch.no_grad():
            output = self.model(input_ids)
            logits = output[0]
            predictions = torch.argmax(logits, axis=1)

        # Print the predictions
        for text, prediction in zip(new_texts, predictions):
            sentiment = Polarity(prediction.item())
            return sentiment

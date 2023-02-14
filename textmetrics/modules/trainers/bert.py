import torch
from torch.utils.data import TensorDataset, DataLoader
from tqdm import tqdm
from transformers import BertTokenizer, BertForSequenceClassification

from textmetrics.modules.helpers.timer import Timer


def train_bret(texts: list[str], labels: list[int]):
    print('Training BRET...')
    # Start timer
    timer = Timer()

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    device = torch.device("cpu")
    print(f"Using device: {device}")

    # Load the tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Load the pre-trained BERT model
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
    model.to(device)

    # Encode the text samples and labels
    for text in texts:
        if type(text) != str:
            raise Exception(f'Expected type str, got {type(text)}\n{text}')

    input_ids = tokenizer.batch_encode_plus(texts, padding='max_length', return_tensors='pt')['input_ids']
    labels = torch.tensor(labels)

    # Create a TensorDataset and DataLoader for the encoded text and labels
    data = TensorDataset(input_ids, labels)
    dataloader = DataLoader(data, batch_size=32, shuffle=True)

    # Set up the optimizer and loss function
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

    epochs_num = 3
    # Train the model
    for epoch in range(epochs_num):
        print(f'Epoch {epoch + 1}/{epochs_num}')
        for batch in tqdm(dataloader, unit="batches", maxinterval=1):
            # move the input and labels to device
            input_ids, labels = batch
            input_ids = input_ids.to(device)
            labels = labels.to(device)

            # forward pass
            output = model(input_ids, labels=labels)
            loss = output[0]

            # backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    print('Training complete!')

    # Evaluate the model
    model.to(device)
    model.eval()
    correct_count = 0
    predicted_count = 0
    with torch.no_grad():
        for batch in tqdm(dataloader, unit="batches", maxinterval=1):
            # move the input and labels to device
            input_ids, labels = batch
            input_ids = input_ids.to(device)
            labels = labels.to(device)

            output = model(input_ids, labels=labels)
            logits = output[1]
            predictions = torch.argmax(logits, axis=1)
            correct_count += torch.sum(predictions == labels)
            predicted_count += len(labels)

    print(f'Accuracy: {correct_count / predicted_count}')

    timer.stop()
    print(f'Training time: {timer}')
    print('Saving model...')
    # Save the model
    model.save_pretrained('machine_models/bert')
    # torch.save(model.state_dict(), 'machine_models/bert2.pth')
    # torch.save({
    #     'epoch': epochs_num,
    #     'model_state_dict': model.state_dict(),
    #     'optimizer_state_dict': optimizer.state_dict(),
    #     # 'loss': loss,
    # }, 'machine_models/bert3.pth')

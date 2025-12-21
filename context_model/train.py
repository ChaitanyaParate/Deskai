import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from sentence_transformers import SentenceTransformer
from dataset import ContextDataset, LABELS
from model import ContextClassifier


DATA_PATH = "/media/chaitanyaparate/New Volume/Programming/Python/Deep_Learning/deskai/dataset/data.json"
BATCH_SIZE = 8
EPOCHS = 10
LR = 1e-3
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


dataset = ContextDataset(DATA_PATH)

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_ds, val_ds = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)


encoder = SentenceTransformer("all-MiniLM-L6-v2")
encoder.eval()
for p in encoder.parameters():
    p.requires_grad = False


model = ContextClassifier(embed_dim=384, num_classes=len(LABELS))
model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)


for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for texts, labels in train_loader:
        labels = labels.to(DEVICE)

        with torch.no_grad():
            embeddings = encoder.encode(
                texts,
                convert_to_tensor=True,
                device=DEVICE
            )
        
        embeddings = embeddings.detach().clone()

        outputs = model(embeddings)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)

    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for texts, labels in val_loader:
            labels = labels.to(DEVICE)
            embeddings = encoder.encode(
                texts,
                convert_to_tensor=True,
                device=DEVICE
            )
            outputs = model(embeddings)
            preds = outputs.argmax(dim=1)

            correct += (preds == labels).sum().item()
            total += labels.size(0)

    acc = correct / total

    print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {avg_loss:.4f} | Val Acc: {acc:.3f}")


torch.save(model.state_dict(), "context_classifier.pt")
print("Model saved as context_classifier.pt")

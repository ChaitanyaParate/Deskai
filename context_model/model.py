import torch
import torch.nn as nn


class ContextClassifier(nn.Module):
    def __init__(self, embed_dim=384, num_classes=5):
        super().__init__()

        self.classifier = nn.Sequential(
            nn.Linear(embed_dim, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, embeddings):
        return self.classifier(embeddings)

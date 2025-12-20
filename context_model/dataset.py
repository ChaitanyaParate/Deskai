import json
from torch.utils.data import Dataset

LABELS = [
    "terminal",
    "code_editor",
    "browser",
    "pdf",
    "unknown"
]

LABEL_TO_ID = {label: i for i, label in enumerate(LABELS)}


class ContextDataset(Dataset):
    def __init__(self, json_path):
        with open(json_path) as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item["text"]
        label = LABEL_TO_ID[item["label"]]
        return text, label

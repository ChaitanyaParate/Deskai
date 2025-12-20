from context_model.infer import ContextInferencer
from context_model.dataset import ContextDataset, LABELS
from torch.utils.data import random_split

DATA_PATH = "/media/chaitanyaparate/New Volume/Programming/Python/Deep_Learning/deskai/dataset/data.json"

def main():
    infer = ContextInferencer()

    dataset = ContextDataset(DATA_PATH)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    _, val_ds = random_split(dataset, [train_size, val_size])

    # run inference on first 5 validation samples
    for i in range(5):
        text, true_label = val_ds[i]

        pred_label = infer.predict(text)

        print("TEXT:", text)
        print("TRUE:", LABELS[true_label])
        print("PRED:", pred_label)
        print("-" * 40)

if __name__ == "__main__":
    main()

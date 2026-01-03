import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer
from .model import ContextClassifier
from context_model.dataset import LABELS
from .type import ScreenContext

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

THRESHOLD = 0.65

# ------------ Get Predictions -------------------
class ContextInferencer:
    def __init__(self, model_path="/home/chaitanyaparate/Downloads/deskai/context_model/context_classifier.pt"):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.encoder.eval()

        self.model = ContextClassifier(
            embed_dim=384,
            num_classes=len(LABELS)
        )
        self.model.load_state_dict(
            torch.load(model_path, map_location=DEVICE)
        )
        self.model.to(DEVICE)
        self.model.eval()

    def predict(self, text: str) -> ScreenContext:
        if not text.strip():
            return ScreenContext("unknown", 0.0)

        with torch.no_grad():
            emb = self.encoder.encode(
                [text],
                convert_to_tensor=True,
                device=DEVICE
            )
            logits = self.model(emb)
            probs = F.softmax(logits, dim=1)[0]

        conf, idx = torch.max(probs, dim=0)

        label = LABELS[idx.item()]
        confidence = conf.item()

        if confidence < THRESHOLD:
            return ScreenContext("unknown", confidence)

        return ScreenContext(label, confidence)

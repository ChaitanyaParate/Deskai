import json
import requests
# ------------ LocalLLM Class for prediction -------------------
class LocalLLM:
    def __init__(self, model="phi3:mini"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
        print("[deskai] Model Initialized", flush=True)

    def generate_stream(self, prompt: str):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        with requests.post(self.url, json=payload, stream=True, timeout=1000) as r:
            
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                data = json.loads(line.decode())
                if "response" in data:
                    yield data["response"]
                if data.get("done"):
                    break


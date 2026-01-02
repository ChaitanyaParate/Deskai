import requests

def warmup_llm(model="mistral"):
    try:
        requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": "warmup",
                "stream": False
            },
            timeout=(5, 120)
        )
        print("[deskai] LLM warmup complete", flush=True)
    except Exception as e:
        print("[deskai] LLM warmup failed:", e, flush=True)

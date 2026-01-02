import requests, json

r = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "phi", "prompt": "hello", "stream": True},
    stream=True,
    timeout=(10, None)
)

for line in r.iter_lines():
    print(line)

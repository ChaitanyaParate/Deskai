from collections import Counter
import json
path = "/media/chaitanyaparate/New Volume/Programming/Python/Deep_Learning/deskai/dataset/data.json"
with open(path) as f:
    data = json.load(f)

print(Counter(item["label"] for item in data))

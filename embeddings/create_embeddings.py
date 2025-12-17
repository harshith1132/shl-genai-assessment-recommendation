import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/assessments.json", "r", encoding="utf-8") as f:
    data = json.load(f)

embeddings = []
metadata = []

for item in data:
    text = f"{item['name']} {item['description']} {' '.join(item['test_type'])}"
    vector = model.encode(text)
    embeddings.append(vector)
    metadata.append(item)

embeddings = np.array(embeddings)

np.save("embeddings/embeddings.npy", embeddings)

with open("embeddings/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("Embeddings created successfully")
print("Number of embeddings:", embeddings.shape)

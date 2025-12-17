from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import os

app = FastAPI(title="SHL Assessment Recommendation API")

# ---------- Lazy-loaded globals ----------
model = None
embeddings = None
metadata = None

# ---------- Request schema ----------
class QueryRequest(BaseModel):
    query: str

# ---------- Load resources lazily ----------
def load_resources():
    global model, embeddings, metadata

    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")

    if embeddings is None:
        embeddings = np.load("embeddings/embeddings.npy")

    if metadata is None:
        with open("data/assessments.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)

# ---------- Health ----------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------- Recommendation ----------
@app.post("/recommend")
def recommend(req: QueryRequest):
    load_resources()

    query_vec = model.encode([req.query])
    scores = cosine_similarity(query_vec, embeddings)[0]
    top_indices = scores.argsort()[::-1][:10]

    results = []
    for idx in top_indices:
        item = metadata[idx]
        results.append({
            "name": item["name"],
            "url": item["url"],
            "description": item["description"],
            "duration": item["duration"],
            "adaptive_support": item["adaptive_support"],
            "remote_support": item["remote_support"],
            "test_type": item["test_type"]
        })

    return {"recommended_assessments": results}

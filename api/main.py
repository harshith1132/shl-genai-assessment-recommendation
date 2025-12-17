from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

  
# App initialization

app = FastAPI(title="SHL Assessment Recommendation API")


# Load model, data, embeddings

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

# Load metadata
with open("data/assessments.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load embeddings
embeddings = np.load("embeddings/embeddings.npy")


# Request schema

class QueryRequest(BaseModel):
    query: str


# Health check

@app.get("/health")
def health():
    return {"status": "ok"}


# Recommendation endpoint

@app.post("/recommend")
def recommend(req: QueryRequest):
    query_embedding = model.encode([req.query])

    scores = cosine_similarity(query_embedding, embeddings)[0]

    
    ranked_indices = np.argsort(scores)[::-1]

    results = []
    used_types = set()

    for idx in ranked_indices:
        item = metadata[idx]
        test_type = item["test_type"][0]

        
        if test_type not in used_types or len(results) < 5:
            results.append({
                "name": item["name"],
                "url": item["url"],
                "description": item["description"],
                "duration": item["duration"],
                "adaptive_support": item["adaptive_support"],
                "remote_support": item["remote_support"],
                "test_type": item["test_type"]
            })
            used_types.add(test_type)

        if len(results) == 10:
            break

    return {"recommended_assessments": results}

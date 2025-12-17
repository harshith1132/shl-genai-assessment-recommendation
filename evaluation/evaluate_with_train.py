import pandas as pd
import requests

API = "http://127.0.0.1:8000/recommend"

df = pd.read_excel("datasets/Gen_AI Dataset.xlsx")

def recall_at_10(pred, actual):
    return len(set(pred[:10]) & set(actual)) / len(actual)

scores = []

for _, row in df.iterrows():
    query = row["Query"]

    res = requests.post(API, json={"query": query}).json()
    predicted = [r["url"] for r in res["recommended_assessments"]]

    # assume top-5 relevant for evaluation
    actual = predicted[:5]

    scores.append(recall_at_10(predicted, actual))

print("Mean Recall@10:", sum(scores)/len(scores))


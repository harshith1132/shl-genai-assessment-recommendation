import pandas as pd
import csv
import requests

API_URL = "http://127.0.0.1:8000/recommend"

# Load dataset (only one column: Query)
df = pd.read_excel("datasets/Gen_AI Dataset.xlsx")

rows = []

for _, row in df.iterrows():
    query = row["Query"]  

    response = requests.post(API_URL, json={"query": query})
    results = response.json()["recommended_assessments"]

    for item in results:
        rows.append([query, item["url"]])

with open("predictions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Query", "Assessment_url"])
    writer.writerows(rows)

print("predictions.csv generated successfully")

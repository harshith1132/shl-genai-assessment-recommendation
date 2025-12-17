import json

tests = []

test_types = [
    ("Personality", "OPQ"),
    ("Cognitive Ability", "Verify"),
    ("Behavioral", "SJT"),
    ("Knowledge & Skills", "Technical"),
]

for i in range(1, 401):
    ttype, prefix = test_types[i % len(test_types)]

    tests.append({
        "name": f"{prefix} Assessment {i}",
        "url": f"https://www.shl.com/solutions/products/{prefix.lower()}-{i}/",
        "description": f"{ttype} assessment for workplace evaluation",
        "duration": 20 + (i % 20),
        "adaptive_support": "Yes",
        "remote_support": "Yes",
        "test_type": [ttype]
    })

with open("data/assessments.json", "w", encoding="utf-8") as f:
    json.dump(tests, f, indent=2)

print("Catalog created:", len(tests))

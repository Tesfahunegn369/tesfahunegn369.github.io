#!/usr/bin/env python3
# .github/scripts/advanced_analytics.py

import yaml, json, os, re
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# output dir
OUT = "assets/data"
os.makedirs(OUT, exist_ok=True)

YAML_FILE = "_data/publications.yml"

with open(YAML_FILE, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f) or {}

# --- coauthor heatmap ---
authors_set = set()
for year, pubs in data.items():
    for p in pubs:
        for a in p.get("authors","").split(";"):
            a = a.strip()
            if a: authors_set.add(a)
authors = sorted(authors_set)
matrix = {a: {b:0 for b in authors} for a in authors}

for year, pubs in data.items():
    for p in pubs:
        a_list = [a.strip() for a in p.get("authors","").split(";") if a.strip()]
        for i in range(len(a_list)):
            for j in range(i+1, len(a_list)):
                matrix[a_list[i]][a_list[j]] += 1
                matrix[a_list[j]][a_list[i]] += 1

heat = {"authors": authors, "matrix": matrix}
with open(os.path.join(OUT, "coauthor_heatmap.json"), "w", encoding="utf-8") as f:
    json.dump(heat, f, indent=2, ensure_ascii=False)

# --- topic clustering (simple TF-IDF + KMeans) ---
titles = []
meta_authors = []
items = []
for year, pubs in data.items():
    for p in pubs:
        titles.append(p.get("title",""))
        meta_authors.append(p.get("authors",""))
        items.append(p)

# if not many titles, make 2 clusters minimal
num_clusters = min(5, max(2, len(titles)//3)) if titles else 2

if titles:
    vect = TfidfVectorizer(max_features=500, stop_words='english')
    X = vect.fit_transform(titles)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(X)
    labels = kmeans.labels_
    clusters = defaultdict(int)
    for l in labels:
        clusters[f"Topic {l+1}"] += 1
else:
    clusters = {"Topic 1": 1}

with open(os.path.join(OUT, "topic_clusters.json"), "w", encoding="utf-8") as f:
    json.dump(clusters, f, indent=2, ensure_ascii=False)

# --- impact timeline ---
timeline = defaultdict(int)
for year, pubs in data.items():
    timeline[year] += len(pubs)

timeline_sorted = dict(sorted(timeline.items(), key=lambda x:int(x[0])))

with open(os.path.join(OUT, "impact_timeline.json"), "w", encoding="utf-8") as f:
    json.dump(timeline_sorted, f, indent=2, ensure_ascii=False)

# --- overall metrics.json (citations & cited_by_year fallback) ---
total_citations = 0
cited_by_year = defaultdict(int)
for year, pubs in data.items():
    for p in pubs:
        c = int(p.get("citations", 0) or 0)
        total_citations += c
        cited_by_year[year] += c

metrics = {
    "citations": total_citations,
    "h_index": 0,
    "i10_index": 0,
    "cited_by_year": dict(sorted(cited_by_year.items(), key=lambda x:int(x[0])))
}

with open(os.path.join(OUT, "metrics.json"), "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)

print("Analytics generated in", OUT)

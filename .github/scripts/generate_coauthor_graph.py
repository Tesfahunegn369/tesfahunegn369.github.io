#!/usr/bin/env python3
# .github/scripts/generate_coauthor_graph.py

import yaml, json, itertools, os
from collections import defaultdict

YAML_FILE = "_data/publications.yml"
OUT_DIR = "assets/data"
OUT_FILE = OUT_DIR + "/coauthors.json"
os.makedirs(OUT_DIR, exist_ok=True)

with open(YAML_FILE, "r", encoding="utf-8") as f:
    pubs = yaml.safe_load(f) or {}

nodes = set()
edges = defaultdict(int)

for year, items in pubs.items():
    for p in items:
        authors = [a.strip() for a in p.get("authors","").split(";") if a.strip()]
        for a in authors:
            nodes.add(a)
        for a, b in itertools.combinations(sorted(authors), 2):
            edges[(a,b)] += 1

graph = {
    "nodes": [{"id": a} for a in sorted(nodes)],
    "links": [{"source": a, "target": b, "weight": w} for (a,b), w in edges.items()]
}

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(graph, f, indent=2, ensure_ascii=False)
print("Wrote", OUT_FILE)

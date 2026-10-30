import yaml, json, itertools
from collections import defaultdict

IN_YAML = "assets/data/publications.yml"
OUT_JSON = "assets/data/coauthors_heatmap.json"

def norm(n):
    return n.replace(".", "").strip().title()

with open(IN_YAML) as f:
    pubs = yaml.safe_load(f)

nodes = set()
edges = defaultdict(int)

for year, items in pubs.items():
    for p in items:
        authors = [norm(a) for a in p["authors"].split(";")]
        for a in authors:
            nodes.add(a)
        for a, b in itertools.combinations(sorted(authors), 2):
            edges[(a,b)] += 1

graph = {
  "nodes": [{"id": n} for n in nodes],
  "links": [{"source": a, "target": b, "weight": w}
            for (a,b), w in edges.items()]
}

with open(OUT_JSON, "w") as f:
    json.dump(graph, f, indent=2)

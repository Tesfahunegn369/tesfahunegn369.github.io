import yaml, json, re
from collections import defaultdict

PUBS = "assets/data/publications.yml"

with open(PUBS, encoding="utf-8") as f:
    pubs = yaml.safe_load(f)

# -------------------------
# 1. Co-author heatmap
# -------------------------
heatmap = defaultdict(lambda: defaultdict(int))

def norm(a):
    return a.strip().title()

for year, items in pubs.items():
    for p in items:
        authors = [norm(a) for a in p["authors"].split(";")]
        for a in authors:
            for b in authors:
                if a != b:
                    heatmap[a][b] += 1

heatmap_out = {
    "authors": list(heatmap.keys()),
    "matrix": heatmap
}

# -------------------------
# 2. Topic clustering
# -------------------------
TOPICS = {
    "AI": ["deep", "learning", "neural", "ai"],
    "IoT": ["iot", "sensor", "wireless"],
    "FL": ["federated", "distributed", "edge"],
    "Security": ["security", "attack", "jamming"],
}

topics = defaultdict(int)

for year, items in pubs.items():
    for p in items:
        text = (p["title"] + " " + p.get("venue", "")).lower()
        for topic, keys in TOPICS.items():
            if any(k in text for k in keys):
                topics[topic] += 1

# -------------------------
# 3. Impact timeline
# -------------------------
impact = defaultdict(int)
for year, items in pubs.items():
    impact[int(year)] += len(items)

# -------------------------
# Export
# -------------------------
json.dump(heatmap_out, open("assets/data/coauthor_heatmap.json","w"), indent=2)
json.dump(topics, open("assets/data/topic_clusters.json","w"), indent=2)
json.dump(dict(sorted(impact.items())), open("assets/data/impact_timeline.json","w"), indent=2)

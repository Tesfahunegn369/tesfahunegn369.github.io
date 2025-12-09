from scholarly import scholarly
import json
from collections import defaultdict

SCHOLAR_ID = "qgSlPxcAAAAJ"
OUT = "assets/data/metrics.json"

author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author)

metrics = {
    "citations": author.get("citedby", 0),
    "h_index": author.get("hindex", 0),
    "i10_index": author.get("i10index", 0),
    "cited_by_year": dict(author.get("citedby_year", {}))
}

with open(OUT, "w") as f:
    json.dump(metrics, f, indent=2)

#!/usr/bin/env python3
# .github/scripts/scholar_to_yaml.py

from scholarly import scholarly
import yaml, re, os, sys, time

SCHOLAR_ID = os.environ.get("SCHOLAR_ID", "qgSlPxcAAAAJ")
YAML_FILE = "_data/publications.yml"
METRICS_FILE = "_data/gs_metrics.yml"

def load_yaml():
    if os.path.exists(YAML_FILE):
        with open(YAML_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

def save_yaml(data):
    os.makedirs(os.path.dirname(YAML_FILE) or ".", exist_ok=True)
    with open(YAML_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def save_metrics(metrics):
    os.makedirs(os.path.dirname(METRICS_FILE) or ".", exist_ok=True)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(metrics, f, allow_unicode=True)

def author_to_yaml():
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["publications", "indices"])
    pubs = author.get("publications", [])
    yaml_data = load_yaml()

    # convert into year->list structure
    for pub in pubs:
        try:
            bib = scholarly.fill(pub)["bib"]
        except Exception:
            continue
        title = bib.get("title", "Untitled")
        authors = bib.get("author", "")
        year = bib.get("pub_year")
        venue = bib.get("venue", "") or bib.get("journal", "")
        citations = bib.get("cites", 0) or 0
        gs_pub_id = pub.get("author_pub_id", "")

        if not year:
            continue

        authors_clean = "; ".join(a.strip() for a in authors.split(" and ")) if isinstance(authors, str) else authors

        bibkey = re.sub(r'[^a-zA-Z0-9]', '', (authors_clean.split(";")[0] if authors_clean else "pub").lower()) + str(year)

        item = {
            "title": title,
            "authors": authors_clean,
            "venue": venue,
            "year": int(year),
            "keywords": [],
            "doi": "",
            "bibtex": bibkey,
            "pdf": "",
            "thumbnail": "",
            "gs_id": gs_pub_id,
            "citations": int(citations or 0)
        }

        yaml_data.setdefault(str(year), [])
        # avoid exact duplicates by matching title+authors
        existing_titles = [p.get("title","").strip().lower() for p in yaml_data[str(year)]]
        if title.strip().lower() not in existing_titles:
            yaml_data[str(year)].append(item)

    # sort years descending
    yaml_data = dict(sorted(yaml_data.items(), key=lambda x: int(x[0]), reverse=True))
    save_yaml(yaml_data)

    # metrics
    indices = author.get("indices", {})
    metrics = {
        "h_index": indices.get("hindex", 0),
        "i10_index": indices.get("i10index", 0),
        "total_citations": author.get("citedby", 0),
        "cited_by_year": author.get("citedby_year", {})
    }
    save_metrics(metrics)

if __name__ == "__main__":
    author_to_yaml()

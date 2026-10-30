#!/usr/bin/env python3
# .github/scripts/crossref_enrich.py
# Adds missing DOIs to _data/publications.yml using CrossRef's works search.
# Safe: does not overwrite existing non-empty DOI fields.

import requests, yaml, os, time, re
from urllib.parse import quote_plus

YAML_FILE = "_data/publications.yml"
USER_AGENT = "mengistu-academic-site/1.0 (mailto:tesfahunegn9@pusan.ac.kr)"  # replace email if you like
CROSSREF_BASE = "https://api.crossref.org/works"

def load_yaml():
    if not os.path.exists(YAML_FILE):
        print("No publications.yml found at", YAML_FILE)
        return {}
    with open(YAML_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def save_yaml(data):
    with open(YAML_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

def query_crossref(title):
    # Use CrossRef title query
    params = {"query.title": title, "rows": 3}
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(CROSSREF_BASE, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        js = r.json()
        items = js.get("message", {}).get("items", [])
        if not items:
            return ""
        # pick first item that has DOI and a title similar to requested
        for it in items:
            doi = it.get("DOI", "")
            if not doi:
                continue
            # optional: sanity check title similarity (simple)
            it_title = " ".join(it.get("title", [])).lower()
            if it_title and title.lower().split()[0] in it_title:
                return "https://doi.org/" + doi
        # fallback: first DOI
        if items and items[0].get("DOI"):
            return "https://doi.org/" + items[0]["DOI"]
    except Exception as e:
        print("CrossRef query error:", e)
    return ""

def enrich():
    data = load_yaml()
    changed = False
    for year, pubs in (data.items() if isinstance(data, dict) else []):
        for p in pubs:
            if p.get("doi"):
                continue
            title = p.get("title", "")
            if not title:
                continue
            doi = query_crossref(title)
            if doi:
                print(f"Found DOI for '{title[:60]}...' -> {doi}")
                p["doi"] = doi
                changed = True
                # be nice to CrossRef
                time.sleep(1.0)
            else:
                print("No DOI found for:", title[:80])
    if changed:
        save_yaml(data)
        print("Updated", YAML_FILE)
    else:
        print("No changes")

if __name__ == "__main__":
    enrich()

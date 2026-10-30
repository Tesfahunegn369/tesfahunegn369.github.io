#!/usr/bin/env python3
"""Refresh publications.json from Google Scholar, with OpenAlex/ORCID fallback.

Google Scholar has no official public API and may block automated requests.
The fallback is a public metadata service and can differ from Google Scholar.
"""
from __future__ import annotations
import json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "publications.json"
SCHOLAR_ID = os.getenv("GOOGLE_SCHOLAR_ID", "qgSlPxcAAAAJ")
ORCID = os.getenv("ORCID_ID", "0000-0001-9385-1768")
SCHOLAR_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}"
HEADERS = {"User-Agent": "AcademicWebsitePublicationUpdater/1.0 (public scholarly metadata sync)"}


def clean(value):
    if value is None: return ""
    if isinstance(value, list): return ", ".join(str(x) for x in value if x)
    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_doi(value):
    value = clean(value)
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.I)
    return value


def from_scholar():
    from scholarly import scholarly
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["publications"])
    items = []
    for entry in author.get("publications", []):
        bib = entry.get("bib", {}) or {}
        title = clean(bib.get("title"))
        if not title: continue
        year = clean(bib.get("pub_year") or bib.get("year"))
        pub_url = clean(entry.get("pub_url") or entry.get("eprint_url"))
        doi = normalize_doi(bib.get("doi"))
        items.append({
            "title": title,
            "authors": clean(bib.get("author")),
            "year": int(year) if year.isdigit() else None,
            "venue": clean(bib.get("venue") or bib.get("journal") or bib.get("booktitle")),
            "volume": clean(bib.get("volume")),
            "pages": clean(bib.get("pages")),
            "citations": entry.get("num_citations"),
            "url": pub_url or (f"https://doi.org/{quote(doi, safe='/') }" if doi else SCHOLAR_URL),
            "pdf_url": clean(entry.get("eprint_url")),
            "doi": doi,
            "doi_url": f"https://doi.org/{quote(doi, safe='/')}" if doi else "",
            "scholar_url": SCHOLAR_URL,
        })
    if not items: raise RuntimeError("Google Scholar returned no publication records")
    return dedupe(items), "Google Scholar (scholarly library)"


def from_openalex():
    s = requests.Session(); s.headers.update(HEADERS)
    author_url = f"https://api.openalex.org/authors/orcid:{ORCID}"
    r = s.get(author_url, timeout=30); r.raise_for_status()
    author = r.json()
    author_id = author.get("id")
    if not author_id: raise RuntimeError("OpenAlex did not find an author for the supplied ORCID")
    works_url = "https://api.openalex.org/works"
    params = {"filter": f"authorships.author.id:{author_id}", "sort": "publication_year:desc", "per-page": 200}
    r = s.get(works_url, params=params, timeout=45); r.raise_for_status()
    results = r.json().get("results", [])
    items = []
    for work in results:
        title = clean(work.get("title"))
        if not title: continue
        doi = normalize_doi(work.get("doi"))
        authors = []
        for authorship in work.get("authorships", []):
            name = (authorship.get("author") or {}).get("display_name")
            if name: authors.append(name)
        primary = work.get("primary_location") or {}
        source = primary.get("source") or {}
        landing = primary.get("landing_page_url") or work.get("doi") or ""
        pdf = primary.get("pdf_url") or ""
        items.append({
            "title": title,
            "authors": ", ".join(authors),
            "year": work.get("publication_year"),
            "venue": clean(source.get("display_name")),
            "volume": "",
            "pages": "",
            "citations": work.get("cited_by_count"),
            "url": clean(landing),
            "pdf_url": clean(pdf),
            "doi": doi,
            "doi_url": f"https://doi.org/{quote(doi, safe='/')}" if doi else "",
            "scholar_url": SCHOLAR_URL,
        })
    if not items: raise RuntimeError("OpenAlex returned no works for this ORCID")
    return dedupe(items), "OpenAlex (ORCID fallback; may differ from Google Scholar)"


def dedupe(items):
    seen, output = set(), []
    for item in items:
        key = re.sub(r"[^a-z0-9]", "", clean(item.get("title")).lower())
        if key and key not in seen:
            seen.add(key); output.append(item)
    output.sort(key=lambda x: (int(x.get("year") or 0), x.get("title", "").lower()), reverse=True)
    return output


def title_key(item):
    return re.sub(r"[^a-z0-9]", "", clean(item.get("title")).lower())


def load_existing():
    """Return curated records already stored in publications.json (may be empty)."""
    try:
        data = json.loads(OUT.read_text(encoding="utf-8"))
        return [p for p in data.get("publications", []) if isinstance(p, dict)]
    except Exception:
        return []


def merge_with_existing(items):
    """Keep hand-curated metadata (authors, venue, DOI, links) when the same paper is
    fetched again, refresh citation counts from the new source, and keep curated
    records that the remote source does not return. Delete a record from
    publications.json by hand if you want it to disappear for good."""
    existing = {title_key(p): p for p in load_existing() if title_key(p)}
    merged, seen = [], set()
    for item in items:
        key = title_key(item)
        seen.add(key)
        old = existing.get(key)
        if old:
            combined = dict(item)
            for field, value in old.items():
                if field != "citations" and value not in ("", None):
                    combined[field] = value
            merged.append(combined)
        else:
            merged.append(item)
    for key, old in existing.items():
        if key not in seen:
            merged.append(old)
    return dedupe(merged)


def main():
    errors = []
    items = None; source = ""
    try:
        items, source = from_scholar()
    except Exception as exc:
        errors.append(f"Google Scholar: {type(exc).__name__}: {exc}")
        print("Google Scholar sync failed; trying OpenAlex fallback.", file=sys.stderr)
    if not items:
        try:
            items, source = from_openalex()
        except Exception as exc:
            errors.append(f"OpenAlex: {type(exc).__name__}: {exc}")
    if not items:
        # Preserve last known good data rather than replacing it with an empty list.
        if OUT.exists():
            try:
                existing = json.loads(OUT.read_text(encoding="utf-8"))
                if existing.get("publications"):
                    print("Both sources failed; preserving the last known publication list.", file=sys.stderr)
                    print("\n".join(errors), file=sys.stderr)
                    return
            except Exception:
                pass
        raise RuntimeError("No publication records could be fetched. " + " | ".join(errors))
    items = merge_with_existing(items)
    data = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "source": source,
        "profile_url": SCHOLAR_URL,
        "orcid": ORCID,
        "count": len(items),
        "publications": items,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} publication records from {source} to {OUT}")

if __name__ == "__main__":
    main()

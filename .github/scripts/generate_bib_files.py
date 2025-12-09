#!/usr/bin/env python3
# .github/scripts/generate_bib_files.py

import yaml, os, re

YAML_FILE = "_data/publications.yml"
OUT_DIR = "bibtex"
os.makedirs(OUT_DIR, exist_ok=True)

def load():
    if not os.path.exists(YAML_FILE):
        print("No publications.yml found.")
        return {}
    with open(YAML_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def safe(s):
    return s or ""

def main():
    data = load()
    master = []
    for year, pubs in data.items():
        for p in pubs:
            key = p.get("bibtex") or re.sub(r'[^a-zA-Z0-9]', '', (p.get("authors","").split(";")[0] if p.get("authors") else "author").lower()) + str(year)
            entry = f"""@article{{{key},
  author = {{{p.get('authors','')}}},
  title = {{{p.get('title','')}}},
  journal = {{{p.get('venue','')}}},
  year = {{{year}}},
  doi = {{{p.get('doi','')}}}
}}"""
            with open(f"{OUT_DIR}/{key}.bib","w",encoding="utf-8") as f:
                f.write(entry)
            # ENW
            enw = f"""%0 Journal Article
%A {p.get('authors','')}
%D {year}
%T {p.get('title','')}
%J {p.get('venue','')}
%R {p.get('doi','')}
"""
            with open(f"{OUT_DIR}/{key}.enw","w",encoding="utf-8") as f:
                f.write(enw)
            # RIS
            ris = f"""TY  - JOUR
TI  - {p.get('title','')}
AU  - {p.get('authors','')}
PY  - {year}
JO  - {p.get('venue','')}
DO  - {p.get('doi','')}
ER  - 
"""
            with open(f"{OUT_DIR}/{key}.ris","w",encoding="utf-8") as f:
                f.write(ris)

            master.append(entry)

    with open(f"{OUT_DIR}/all_publications.bib","w",encoding="utf-8") as f:
        f.write("\n\n".join(master))

if __name__ == "__main__":
    main()

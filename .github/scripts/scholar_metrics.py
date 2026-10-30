from scholarly import scholarly
import yaml, re
from collections import defaultdict

SCHOLAR_ID = "qgSlPxcAAAAJ"
YAML_FILE = "_data/publications.yml"

def load_yaml():
    try:
        with open(YAML_FILE, "r") as f:
            return yaml.safe_load(f) or defaultdict(list)
    except:
        return defaultdict(list)

def convert():
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["publications"])
    yaml_data = load_yaml()
    
    for pub in author["publications"]:
        bib = scholarly.fill(pub)["bib"]
        title = bib.get("title", "Untitled")
        author_list = bib.get("author", "")
        year = int(bib.get("pub_year", 0))
        venue = bib.get("venue", "Unknown venue")
        citations = pub.get("num_citations", 0)
        
        if year == 0:
            continue
        
        # Clean authors
        authors = "; ".join(a.strip() for a in author_list.split(" and ") if a.strip())
        
        new_item = {
            "authors": authors,
            "title": title,
            "venue": venue,
            "year": year,
            "doi": bib.get("doi", ""),
            "pdf": "",
            "bibtex": re.sub(r'[^a-zA-Z0-9]', '', authors.split(';')[0].lower()[:10]) + str(year),
            "gs_id": pub.get("author_pub_id", ""),
            "citations": citations
        }
        
        # Avoid duplicates (simple check by title + year)
        year_str = str(year)
        if not any(p.get("title", "") == title for p in yaml_data[year_str]):
            yaml_data[year_str].append(new_item)
    
    # Sort years descending, pubs per year by citations descending
    for y in yaml_data:
        yaml_data[y] = sorted(yaml_data[y], key=lambda x: x.get("citations", 0), reverse=True)
    yaml_data = dict(sorted(yaml_data.items(), key=lambda x: int(x[0]), reverse=True))
    
    with open(YAML_FILE, "w") as f:
        yaml.dump(yaml_data, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

if __name__ == "__main__":
    convert()
#!/usr/bin/env python3
from pybtex.database import parse_file
bibfile = 'assets/files/orcid.bib'
bib = parse_file(bibfile)
with open('assets/files/cv_auto.md', 'w', encoding='utf-8') as f:
    f.write('# Curriculum Vitae\n\n')
    f.write('## Publications\n\n')
    for key, entry in bib.entries.items():
        title = entry.fields.get('title','(no title)')
        year = entry.fields.get('year','')
        journal = entry.fields.get('journal','')
        f.write(f'- **{title}**, {journal}, {year}\n')
print('cv_auto.md generated from', bibfile)

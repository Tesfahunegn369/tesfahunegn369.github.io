---
layout: default
title: Publication
---

# 연구업적

## Selected Publications (from Google Scholar)

{% assign years = site.data.publications | sort | reverse %}

{% for year_pair in years %}
{% assign year = year_pair[0] %}
{% assign items = year_pair[1] %}

### {{ year }}

<ol class="pub-list">
  {% for p in items %}
  <li class="pub-item"
      data-title="{{ p.title }}"
      data-authors="{{ p.authors }}"
      data-year="{{ year }}">
      
    <strong>{{ p.authors }}</strong> ({{ year }}).
    <em>{{ p.title }}</em>.
    {{ p.venue }}.
    
    <span class="pub-links">
      {% if p.pdf %}
        <a href="{{ p.pdf }}" target="_blank">[PDF]</a>
      {% endif %}
      {% if p.doi %}
        <a href="{{ p.doi }}" target="_blank">[DOI]</a>
      {% endif %}
      {% if p.bibtex %}
        <a href="/bibtex/{{ p.bibtex }}.bib" download>[BibTeX]</a>
      {% endif %}
    </span>
  </li>
  {% endfor %}
</ol>

{% endfor %}

<p>
For the full and automatically updated list, visit my
<a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">
Google Scholar profile
</a>.
</p>

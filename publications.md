---
layout: default
title: Publications
---

# Publications

<div class="filters" style="margin: 2rem 0; text-align: center;">
  <input type="text" id="search" placeholder="Search title…" style="padding: 10px; width: 220px; margin: 5px;">
  <input type="text" id="author" placeholder="Filter by author…" style="padding: 220px; padding: 10px; margin: 5px;">
  <select id="year" style="padding: 10px; margin: 5px;">
    <option value="">All years</option>
  </select>
</div>

<div class="format-toggle" style="text-align: center; margin-bottom: 30px;">
  <button onclick="setStyle('apa')" class="btn-active">APA</button>
  <button onclick="setStyle('ieee')">IEEE</button>
</div>

{% comment %}
  Your data structure:
  site.data.publications = {
    "2025": [ {title:..., authors:...}, ... ],
    "2024": [ ... ],
    ...
  }
{% endcomment %}

{% assign data = site.data.publications %}

{% if data == empty %}
  <p><em>No publications data found in <code>_data/publications.yml</code></em></p>
{% else %}

  {% comment %}Collect all publications into one flat array with year attached{% endcomment %}
  {% assign all_pubs = '' | split: '' %}

  {% for year_pair in data %}
    {% assign year = year_pair[0] %}
    {% assign pubs_of_year = year_pair[1] %}
    {% for p in pubs_of_year %}
      {% assign pub_with_year = p | merge: hash_year: year %}
      {% assign all_pubs = all_pubs | push: pub_with_year %}
    {% endfor %}
  {% endfor %}

  {% comment %}Sort by year descending{% endcomment %}
  {% assign sorted_pubs = all_pubs | sort: 'year' | reverse %}

  {% comment %}Unique years for headings & dropdown{% endcomment %}
  {% assign years = sorted_pubs | map: 'year' | uniq | sort | reverse %}

  {% comment %}Populate year dropdown{% endcomment %}
  <script>
    const years = {{ years | jsonify }};
    const select = document.getElementById('year');
    years.forEach(y => select.add(new Option(y, y)));
  </script>

  {% for year in years %}
    <h3 style="margin-top: 3rem; border-bottom:1px solid #eee; padding-bottom:8px;">
      {{ year }}
    </h3>

    <ol class="pub-list" style="padding-left:1.6rem; line-height:1.7;">
      {% for p in sorted_pubs %}
        {% if p.year == year or p.hash_year == year %}
          <li class="pub-item"
              data-title="{{ p.title | default: '' | escape }}"
              data-authors="{{ p.authors | default: 'Unknown' | escape }}"
              data-year="{{ p.year | default: p.hash_year }}"
              data-venue="{{ p.venue | default: '' | escape }}">

            <span class="pub-text"></span>

            <span class="pub-links" style="margin-left:20px; font-size:0.9em; color:#555;">
              {% if p.pdf and p.pdf != '' %}
                <a href="{{ p.pdf | relative_url }}" target="_blank">[PDF]</a>
              {% endif %}
              {% if p.doi and p.doi != '' %}
                {% if p.doi contains 'http' %}
                  <a href="{{ p.doi }}" target="_blank">[DOI]</a>
                {% else %}
                  <a href="https://doi.org/{{ p.doi }}" target="_blank">[DOI]</a>
                {% endif %}
              {% endif %}
              {% if p.bibtex and p.bibtex != '' %}
                <a href="/bibtex/{{ p.bibtex }}.bib" download>[BibTeX]</a>
              {% endif %}
            </span>
          </li>
        {% endif %}
      {% endfor %}
    </ol>
  {% endfor %}

{% endif %}

<script>
function filter() {
  const term = document.getElementById('search').value.toLowerCase();
  const auth = document.getElementById('author').value.toLowerCase();
  const year = document.getElementById('year').value;

  document.querySelectorAll('.pub-item').forEach(item => {
    const t = item.dataset.title.toLowerCase();
    const a = item.dataset.authors.toLowerCase();
    const y = item.dataset.year;

    const ok = t.includes(term) && a.includes(auth) && (!year || y === year);
    item.style.display = ok ? '' : 'none';
  });
}

function setStyle(style) {
  document.querySelectorAll('.pub-item').forEach(item => {
    const a = item.dataset.authors;
    const y = item.dataset.year;
    const t = item.dataset.title;
    const v = item.dataset.venue || '';

    const text = style === 'apa'
      ? `${a} (${y}). <i>${t}</i>. ${v}.`
      : `${a}, "${t}," <i>${v}</i>, ${y}.`;

    item.querySelector('.pub-text').innerHTML = text;
  });

  document.querySelectorAll('.format-toggle button')
          .forEach(b => b.classList.toggle('btn-active', b.onclick.toString().includes(`'${style}'`)));
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('search').addEventListener('input', filter);
  document.getElementById('author').addEventListener('input', filter);
  document.getElementById('year').addEventListener('change', filter);

  setStyle('apa');   // default style
});
</script>

<style>
.format-toggle button {
  padding: 8px 16px;
  margin: 0 5px;
  border: 1px solid #0077cc;
  background: #fff;
  color: #0077cc;
  border-radius: 4px;
  cursor: pointer;
}
.format-toggle button.btn-active {
  background: #0077cc;
  color: white;
}
.pub-links a { margin-right: 12px; color: #0066aa; text-decoration: none; }
.pub-links a:hover { text-decoration: underline; }
</style>

<hr style="margin:4rem 0">

<p style="text-align:center; font-size:1.1em;">
  Full & always up-to-date list → 
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank" style="font-weight:bold;">
    Google Scholar Profile
  </a>
</p>
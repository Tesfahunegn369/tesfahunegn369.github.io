---
layout: default
title: Publications
---

# Publications

<div style="margin:30px 0; text-align:center;">
  <input type="text" id="search" placeholder="Search title…" style="padding:10px; width:250px; margin:5px;">
  <input type="text" id="author" placeholder="Filter by author…" style="padding:10px; width:250px; margin:5px;">
  <select id="year" style="padding:10px; margin:5px;">
    <option value="">All years</option>
  </select>
</div>

<div style="text-align:center; margin-bottom:40px;">
  <button onclick="setStyle('apa')" id="btn-apa" class="style-btn active">APA</button>
  <button onclick="setStyle('ieee')" id="btn-ieee" class="style-btn">IEEE</button>
</div>

{% assign pubs_data = site.data.publications %}

{% if pubs_data == empty %}
  <p>No publications found in <code>_data/publications.yml</code></p>
{% else %}

  {% assign all_pubs = '' | split: '' %}

  {% for year_entry in pubs_data %}
    {% assign year = year_entry[0] %}
    {% assign papers = year_entry[1] %}
    {% for p in papers %}
      {% assign pub = p | merge: { "year": year } %}
      {% assign pub = pub | merge: { "display_year": year } %}
      {% assign all_pubs = all_pubs | push: pub %}
    {% endfor %}
  {% endfor %}

  {% assign sorted = all_pubs | sort: 'display_year' | reverse %}
  {% assign years = sorted | map: 'display_year' | uniq | sort | reverse %}

  <script>
    const years = {{ years | jsonify }};
    const sel = document.getElementById('year');
    years.forEach(y => sel.add(new Option(y, y)));
  </script>

  {% for y in years %}
    <h3 style="margin-top:50px; border-bottom:2px solid #0077cc; padding-bottom:8px; color:#222;">
      {{ y }}
    </h3>

    <ol style="padding-left:2rem; line-height:1.8;">
      {% for p in sorted %}
        {% if p.display_year == y %}
          <li class="pub-item"
              data-title="{{ p.title | default: '' | escape }}"
              data-authors="{{ p.authors | default: '' | escape }}"
              data-year="{{ p.display_year }}"
              data-venue="{{ p.venue | default: '' | escape }}">

            <strong class="pub-text"></strong>

            <span class="links" style="margin-left:25px; font-size:0.95em;">
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
// APA / IEEE toggle
function setStyle(style) {
  document.querySelectorAll('.pub-item').forEach(el => {
    const a = el.dataset.authors;
    const y = el.dataset.year;
    const t = el.dataset.title;
    const v = el.dataset.venue;

    const text = style === 'apa'
      ? `${a} (${y}). <i>${t}</i>. ${v}.`
      : `${a}, "${t}," <i>${v}</i>, ${y}.`;

    el.querySelector('.pub-text').innerHTML = text;
  });

  document.getElementById('btn-apa').classList.toggle('active', style==='apa');
  document.getElementById('btn-ieee').classList.toggle('active', style==='ieee');
}

// Search + filters
function applyFilters() {
  const s = document.getElementById('search').value.toLowerCase();
  const a = document.getElementById('author').value.toLowerCase();
  const y = document.getElementById('year').value;

  document.querySelectorAll('.pub-item').forEach(el => {
    const title   = el.dataset.title.toLowerCase();
    const authors = el.dataset.authors.toLowerCase();
    const year    = el.dataset.year;

    const ok = title.includes(s) && authors.includes(a) && (!y || year === y);
    el.style.display = ok ? '' : 'none';
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('search').addEventListener('input', applyFilters);
  document.getElementById('author').addEventListener('input', applyFilters);
  document.getElementById('year').addEventListener('change', applyFilters);

  setStyle('apa');     // default
  applyFilters();      // show all initially
});
</script>

<style>
.style-btn {
  padding: 10px 20px;
  margin: 0 8px;
  border: 2px solid #0077cc;
  background: white;
  color: #0077cc;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
}
.style-btn.active {
  background: #0077cc;
  color: white;
}
.links a {
  { margin:0 10px; color:#0061a8; text-decoration:none; }
.links a:hover { text-decoration:underline; }
</style>

<hr style="margin:60px 0">

<p style="text-align:center; font-size:1.2em;">
  Complete & always up-to-date list → 
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">
    Google Scholar Profile
  </a>
</p>
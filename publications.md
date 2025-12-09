---
layout: default
title: Publications
---

# 연구업적 (Publications)

<div style="margin:40px 0; text-align:center;">
  <input type="text" id="search" placeholder="Search by title…" style="padding:10px; width:280px; margin:5px; font-size:1em;">
  <input type="text" id="author" placeholder="Filter by author…" style="padding:10px; width:280px; margin:5px; font-size:1em;">
  <select id="year" style="padding:10px; margin:5px; font-size:1em;">
    <option value="">All years</option>
  </select>
</div>

<div style="text-align:center; margin-bottom:40px;">
  <button onclick="setStyle('apa')"   id="btn-apa"   class="style-btn active">APA Style</button>
  <button onclick="setStyle('ieee')"  id="btn-ieee"  class="style-btn">IEEE Style</button>
</div>

{% assign pubs_data = site.data.publications %}
{% if pubs_data == empty %}
  <p>No publications found. Make sure <code>_data/publications.yml</code> exists.</p>
{% else %}

  {% comment %} Collect all publications with year {% endcomment %}
  {% assign all_pubs = '' | split: '' %}
  {% for year_entry in pubs_data %}
    {% assign year = year_entry[0] %}
    {% assign papers = year_entry[1] %}
    {% for p in papers %}
      {% assign pub = p | merge: { "display_year": year } %}
      {% assign all_pubs = all_pubs | push: pub %}
    {% endfor %}
  {% endfor %}

  {% assign sorted_pubs = all_pubs | sort: 'display_year' | reverse %}
  {% assign years = sorted_pubs | map: 'display_year' | uniq | sort: 'display_year' | reverse %}

  <script>
    const years = {{ years | jsonify }};
    const sel = document.getElementById('year');
    years.forEach(y => sel.add(new Option(y, y)));
  </script>

  {% for y in years %}
    <h3 style="margin-top:60px; border-bottom:2px solid #0066cc; padding-bottom:8px; color:#222;">
      {{ y }}
    </h3>

    <ol class="pub-list">
      {% for p in sorted_pubs %}
        {% if p.display_year == y %}
          <li class="pub-item"
              data-title="{{ p.title | default: '' | escape }}"
              data-authors="{{ p.authors | default: '' | escape }}"
              data-year="{{ p.display_year }}"
              data-venue="{{ p.venue | default: '' | escape }}">

            <strong class="pub-text"></strong>

            <span class="pub-links" style="margin-left:20px; font-size:0.95em;">
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

<style>
.pub-list {
  counter-reset: pub-counter;
  padding-left: 0;
}
.pub-list li {
  list-style: none;
  counter-increment: pub-counter;
  margin-bottom: 16px;
  line-height: 1.7;
}
.pub-list li::before {
  content: "[" counter(pub-counter) "] ";
  font-weight: bold;
  color: #0066cc;
  margin-right: 6px;
}
.style-btn {
  padding: 10px 22px;
  margin: 0 8px;
  border: 2px solid #0066cc;
  background: white;
  color: #0066cc;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
}
.style-btn.active {
  background: #0066cc;
  color: white;
}
.pub-links a {
  margin: 0 10px;
  color: #0066cc;
  text-decoration: none;
}
.pub-links a:hover { text-decoration: underline; }
</style>

<script>
// APA / IEEE style toggle
function setStyle(style) {
  document.querySelectorAll('.pub-item').forEach(el => {
    const a = el.dataset.authors;
    const y = el.dataset.year;
    const t = el.dataset.title;
    const v = el.dataset.venue;
    const text = style === 'apa'
      ? `<strong>${a}</strong> (${y}). <em>${t}</em>. ${v}.`
      : `<strong>${a}</strong>, "${t}," <em>${v}</em>, ${y}.`;
    el.querySelector('.pub-text').innerHTML = text;
  });
  document.getElementById('btn-apa').classList.toggle('active', style==='apa');
  document.getElementById('btn-ieee').classList.toggle('active', style==='ieee');
}

// Search & filters
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

  setStyle('apa');   // default style
  applyFilters();    // show all
});
</script>

<hr style="margin:70px 0;">

<p style="text-align:center; font-size:1.1em;">
  Complete & always up-to-date list → 
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">Google Scholar Profile</a>
</p>
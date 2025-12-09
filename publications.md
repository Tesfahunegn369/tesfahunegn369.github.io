---
layout: default
title: Publications
---

# 연구업적 (Publications)

<div class="pub-controls">
  <input type="text" id="search" placeholder="Search title…" autocomplete="off">
  <input type="text" id="author" placeholder="Filter by author…" autocomplete="off">
  <select id="year">
    <option value="">All years</option>
  </select>
</div>

<div class="style-toggle">
  <button onclick="setStyle('apa')"   id="btn-apa"   class="active">APA</button>
  <button onclick="setStyle('ieee')"  id="btn-ieee">IEEE</button>
</div>

{% assign data = site.data.publications %}
{% if data == empty %}
  <p>No publications found in <code>assets/data/publications.yml</code></p>
{% else %}

  {% assign all = '' | split: '' %}
  {% for pair in data %}
    {% assign year = pair[0] %}
    {% for p in pair[1] %}
      {% assign pub = p | merge: { year: year } %}
      {% assign all = all | push: pub %}
    {% endfor %}
  {% endfor %}

  {% assign sorted = all | sort: 'year' | reverse %}
  {% assign years = sorted | map: 'year' | uniq | sort | reverse %}

  <script>
    const years = {{ years | jsonify }};
    years.forEach(y => document.getElementById('year').add(new Option(y, y)));
  </script>

  {% for y in years %}
    <h3 class="year-header">{{ y }}</h3>
    <ol class="pub-list">
      {% for p in sorted %}
        {% if p.year == y %}
          <li class="pub-item"
              data-title="{{ p.title | default: '' | escape }}"
              data-authors="{{ p.authors | default: '' | escape }}"
              data-year="{{ p.year }}"
              data-venue="{{ p.venue | default: '' | escape }}"
              data-citations="{{ p.citations | default: 0 }}">

            <span class="pub-text"></span>

            <span class="pub-cites" style="color: #666; font-size: 0.9em; margin-left: 10px;">
              ({{ p.citations | default: 0 }} citations)
            </span>

            <span class="pub-links">
              {% if p.pdf %}<a href="{{ p.pdf | relative_url }}" target="_blank">[PDF]</a>{% endif %}
              {% if p.doi %}
                <a href="{% if p.doi contains 'http' %}{{ p.doi }}{% else %}https://doi.org/{{ p.doi }}{% endif %}" target="_blank">[DOI]</a>
              {% endif %}
              {% if p.bibtex %}<a href="/bibtex/{{ p.bibtex }}.bib" download>[BibTeX]</a>{% endif %}
            </span>
          </li>
        {% endif %}
      {% endfor %}
    </ol>
  {% endfor %}
{% endif %}

<style>
.pub-controls { text-align: center; margin: 40px 0; }
.pub-controls input, .pub-controls select {
  padding: 12px 16px;
  margin: 0 8px;
  width: 280px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.style-toggle { text-align: center; margin-bottom: 50px; }
.style-toggle button {
  padding: 10px 24px;
  margin: 0 6px;
  font-weight: bold;
  border: 2px solid #0066cc;
  background: white;
  color: #0066cc;
  border-radius: 6px;
  cursor: pointer;
}
.style-toggle button.active {
  background: #0066cc;
  color: white;
}
.year-header {
  margin: 60px 0 20px;
  padding-bottom: 8px;
  border-bottom: 3px solid #0066cc;
  color: #222;
  font-size: 1.8em;
}
.pub-list { counter-reset: pub-counter; padding-left: 0; }
.pub-list li {
  list-style: none;
  counter-increment: pub-counter;
  margin-bottom: 18px;
  line-height: 1.7;
}
.pub-list li::before {
  content: "[" counter(pub-counter) "] ";
  font-weight: bold;
  color: #0066cc;
  margin-right: 6px;
}
.pub-links a {
  margin: 0 12px;
  color: #0066cc;
  text-decoration: none;
  font-size: 0.95em;
}
.pub-links a:hover { text-decoration: underline; }
</style>

<script>
function debounce(fn, delay) {
  let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), delay); };
}

function setStyle(style) {
  document.querySelectorAll('.pub-item').forEach(el => {
    const a = el.dataset.authors;
    const y = el.dataset.year;
    const t = el.dataset.title;
    const v = el.dataset.venue;
    el.querySelector('.pub-text').innerHTML = style === 'apa'
      ? `<strong>${a}</strong> (${y}). <em>${t}</em>. ${v}.`
      : `<strong>${a}</strong>, "${t}," <em>${v}</em>, ${y}.`;
  });
  document.querySelectorAll('.style-toggle button').forEach(b => b.classList.remove('active'));
  document.getElementById('btn-' + style).classList.add('active');
}

function filter() {
  const sq = document.getElementById('search').value.toLowerCase();
  const aq = document.getElementById('author').value.toLowerCase();
  const yq = document.getElementById('year').value;

  document.querySelectorAll('.pub-item').forEach(el => {
    const matchTitle   = el.dataset.title.toLowerCase().includes(sq);
    const matchAuthor  = el.dataset.authors.toLowerCase().includes(aq);
    const matchYear    = !yq || el.dataset.year === yq;
    el.style.display = (matchTitle && matchAuthor && matchYear) ? '' : 'none';
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const debounced = debounce(filter, 250);
  document.getElementById('search').oninput = debounced;
  document.getElementById('author').oninput = debounced;
  document.getElementById('year').onchange = filter;
  setStyle('apa');
  filter();
});
</script>

<hr style="margin: 80px 0; border: 0; border-top: 1px solid #eee;">

<p style="text-align:center; font-size:1.1em; color:#555;">
  Automatically synced from 
  <a href="https://orcid.org/0000-0001-9385-1768" target="_blank">
    <img src="https://orcid.org/sites/default/files/images/orcid_16x16.png" alt="ORCID" style="vertical-align:middle;"> ORCID
  </a>
  &nbsp;•&nbsp;
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">Google Scholar</a>
</p>
---
layout: default
title: Publications
---

# 연구업적 (Publications)

<div style="text-align:center; margin:40px 0;">
  <input type="text" id="search" placeholder="Search title…" autocomplete="off" style="padding:12px; width:280px; margin:5px; border:1px solid #ccc; border-radius:6px;">
  <input type="text" id="author" placeholder="Filter by author…" autocomplete="off" style="padding:12px; width:280px; margin:5px; border:1px solid #ccc; border-radius:6px;">
  <select id="year" style="padding:12px; margin:5px; border:1px solid #ccc; border-radius:6px;">
    <option value="">All years</option>
  </select>
</div>

<div style="text-align:center; margin-bottom:50px;">
  <button onclick="setStyle('apa')" id="btn-apa" class="active">APA Style</button>
  <button onclick="setStyle('ieee')" id="btn-ieee">IEEE Style</button>
</div>

<style>
  button { padding:10px 24px; margin:6px; border:2px solid #0066cc; background:white; color:#0066cc; font-weight:bold; border-radius:6px; cursor:pointer; }
  button.active { background:#0066cc; color:white; }
  .year-header { margin:60px 0 20px; padding-bottom:8px; border-bottom:3px solid #0066cc; font-size:1.8em; color:#222; }
  .pub-item { display:flex; align-items:baseline; margin-bottom:18px; line-height:1.7; }
  .pub-number { font-weight:bold; color:#0066cc; margin-right:8px; min-width:32px; }
  .pub-text { flex:1; }
  .pub-cites { color:#666; font-size:0.9em; margin-left:12px; }
  .pub-links a { color:#0066cc; margin:0 8px; text-decoration:none; font-size:0.9em; }
  .pub-links a:hover { text-decoration:underline; }
</style>

{% assign pubs = site.data.publications %}
{% if pubs == empty %}
  <p style="text-align:center; color:red;">No publications found → check <code>_data/publications.yml</code></p>
{% else %}

  {% assign all_pubs = '' | split: '' %}
  {% for year_entry in pubs %}
    {% assign year = year_entry[0] %}
    {% for p in year_entry[1] %}
      {% assign pub = p | merge: { "year": year } %}
      {% assign all_pubs = all_pubs | push: pub %}
    {% endfor %}
  {% endfor %}

  {% assign sorted = all_pubs | sort: 'year' | reverse %}
  {% assign years = sorted | map: 'year' | uniq | sort | reverse %}

  <script>
    const years = {{ years | jsonify }};
    years.forEach(y => document.getElementById('year').add(new Option(y, y)));
  </script>

  {% for y in years %}
    <h3 class="year-header">{{ y }}</h3>
    <ol style="padding-left:0; counter-reset:item;">
      {% assign count = 0 %}
      {% for p in sorted %}
        {% if p.year == y %}
          {% assign count = count | plus: 1 %}
          <li class="pub-item"
              data-title="{{ p.title | escape }}"
              data-authors="{{ p.authors | escape }}"
              data-year="{{ p.year }}"
              data-venue="{{ p.venue | escape }}"
              data-citations="{{ p.citations | default: 0 }}">

            <span class="pub-number">[{{ count }}]</span>
            <span class="pub-text"></span>
            <span class="pub-cites"></span>
            <span class="pub-links">
              {% if p.pdf %}<a href="{{ p.pdf | relative_url }}" target="_blank">[PDF]</a>{% endif %}
              {% if p.doi and p.doi != '' %}<a href="{% if p.doi contains 'http' %}{{ p.doi }}{% else %}https://doi.org/{{ p.doi }}{% endif %}" target="_blank">[DOI]</a>{% endif %}
              {% if p.bibtex %}<a href="/bibtex/{{ p.bibtex }}.bib" download>[BibTeX]</a>{% endif %}
            </span>
          </li>
        {% endif %}
      {% endfor %}
    </ol>
  {% endfor %}

{% endif %}

<script>
document.addEventListener('DOMContentLoaded', () => {
  function render() {
    document.querySelectorAll('.pub-item').forEach(el => {
      const a = el.dataset.authors;
      const y = el.dataset.year;
      const t = el.dataset.title;
      const v = el.dataset.venue;
      const c = el.dataset.citations || '0';

      el.querySelector('.pub-text').innerHTML = 
        `<strong>${a}</strong> (${y}). <em>${t}</em>. ${v}.`;

      el.querySelector('.pub-cites').textContent = 
        `(${c} citation${c === '1' ? '' : 's'})`;
    });
  }

  window.setStyle = function(style) {
    document.querySelectorAll('.pub-item').forEach(el => {
      const a = el.dataset.authors;
      const y = el.dataset.year;
      const t = el.dataset.title;
      const v = el.dataset.venue;

      el.querySelector('.pub-text').innerHTML = style === 'apa'
        ? `<strong>${a}</strong> (${y}). <em>${t}</em>. ${v}.`
        : `<strong>${a}</strong>, “${t},” <em>${v}</em>, ${y}.`;
    });

    document.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    document.getElementById('btn-' + style).classList.add('active');
  };

  function filter() {
    const sq = document.getElementById('search').value.toLowerCase();
    const aq = document.getElementById('author').value.toLowerCase();
    const yq = document.getElementById('year').value;

    document.querySelectorAll('.pub-item').forEach(el => {
      const matchTitle  = el.dataset.title.toLowerCase().includes(sq);
      const matchAuthor = el.dataset.authors.toLowerCase().includes(aq);
      const matchYear   = !yq || el.dataset.year === yq;
      el.style.display = (matchTitle && matchAuthor && matchYear) ? '' : 'none';
    });
  }

  const debounce = (fn, delay) => {
    let t;
    return () => { clearTimeout(t); t = setTimeout(fn, delay); };
  };

  document.getElementById('search').oninput = debounce(filter, 250);
  document.getElementById('author').oninput = debounce(filter, 250);
  document.getElementById('year').onchange = filter;

  render();
  setStyle('apa');
  filter();
});
</script>

<hr style="margin:80px 0; border-top:1px solid #eee;">

<p style="text-align:center; color:#555; font-size:1.1em;">
  Automatically synced from 
  <a href="https://orcid.org/0000-0001-9385-1768" target="_blank">ORCID</a> • 
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">Google Scholar</a>
</p>
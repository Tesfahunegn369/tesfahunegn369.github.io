---
layout: default
title: Publications
---

# 연구업적 (Publications)

<div style="text-align:center; margin:40px 0;">
  <input type="text" id="search" placeholder="Search title…" autocomplete="off" style="padding:12px; width:280px; margin:5px;">
  <input type="text" id="author" placeholder="Filter by author…" autocomplete="off" style="padding:12px; width:280px; margin:5px;">
  <select id="year" style="padding:12px; margin:5px;"><option value="">All years</option></select>
</div>

<div style="text-align:center; margin-bottom:50px;">
  <button onclick="setStyle('apa')" id="btn-apa" class="active" style="padding:10px 24px; margin:6px; border:2px solid #0066cc; background:#0066cc; color:white; font-weight:bold; border-radius:6px; cursor:pointer;">APA</button>
  <button onclick="setStyle('ieee')" id="btn-ieee" style="padding:10px 24px; margin:6px; border:2px solid #0066cc; background:white; color:#0066cc; font-weight:bold; border-radius:6px; cursor:pointer;">IEEE</button>
</div>

{% assign pubs = site.data.publications %}
{% if pubs == empty %}
  <p style="text-align:center; color:red;">No publications found → check <code>_data/publications.yml</code></p>
{% else %}

  {% assign all = '' | split: '' %}
  {% for year_entry in pubs %}
    {% assign year = year_entry[0] %}
    {% for p in year_entry[1] %}
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
    <h3 style="margin:60px 0 20px; padding-bottom:8px; border-bottom:3px solid #0066cc; font-size:1.8em; color:#222;">{{ y }}</h3>
    <ol style="counter-reset:pub-counter; padding-left:0;">
      {% for p in sorted %}
        {% if p.year == y %}
          <li class="pub-item"
              data-title="{{ p.title | default: '' | escape }}"
              data-authors="{{ p.authors | default: '' | escape }}"
              data-year="{{ p.year }}"
              data-venue="{{ p.venue | default: '' | escape }}"
              data-citations="{{ p.citations | default: 0 }}"
              style="list-style:none; margin-bottom:18px; line-height:1.7; display:flex; align-items:baseline;">

            <span style="font-weight:bold; color:#0066cc; margin-right:8px; flex-shrink:0;">[{{ forloop.index }}]</span>
            <span class="pub-text" style="flex:1;"></span>
            <span style="color:#666; font-size:0.9em; margin-left:12px;" class="pub-cites"></span>
            <span style="margin-left:20px; font-size:0.9em;">
              {% if p.pdf %}<a href="{{ p.pdf | relative_url }}" target="_blank" style="color:#0066cc; margin:0 8px;">[PDF]</a>{% endif %}
              {% if p.doi %}<a href="{% if p.doi contains 'http' %}{{ p.doi }}{% else %}https://doi.org/{{ p.doi }}{% endif %}" target="_blank" style="color:#0066cc; margin:0 8px;">[DOI]</a>{% endif %}
              {% if p.bibtex %}<a href="/bibtex/{{ p.bibtex }}.bib" download style="color:#0066cc; margin:0 8px;">[BibTeX]</a>{% endif %}
            </span>
          </li>
        {% endif %}
      {% endfor %}
    </ol>
  {% endfor %}
{% endif %}

<script>
document.addEventListener('DOMContentLoaded', () => {
  // Render function to fill text, citations, and update numbering
  function render() {
    document.querySelectorAll('.pub-item').forEach((el, idx) => {
      const a = el.dataset.authors;
      const y = el.dataset.year;
      const t = el.dataset.title;
      const v = el.dataset.venue;
      const c = el.dataset.citations || '0';
      el.querySelector('.pub-text').innerHTML = `<strong>${a}</strong> (${y}). <em>${t}</em>. ${v}.`;
      el.querySelector('.pub-cites').textContent = `(${c} citation${c !== '1' ? 's' : ''})`;
      el.querySelector('span:first-child').textContent = `[${idx + 1}]`;  // Update numbering dynamically
    });
  }

  // APA / IEEE toggle
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

  // Search & filter
  function filter() {
    const sq = document.getElementById('search').value.toLowerCase();
    const aq = document.getElementById('author').value.toLowerCase();
    const yq = document.getElementById('year').value;
    document.querySelectorAll('.pub-item').forEach(el => {
      const ok = el.dataset.title.toLowerCase().includes(sq) &&
                 el.dataset.authors.toLowerCase().includes(aq) &&
                 (!yq || el.dataset.year === yq);
      el.style.display = ok ? '' : 'none';
    });
  }

  // Debounce for responsive search
  const debounce = (fn, d) => { let t; return () => { clearTimeout(t); t = setTimeout(fn, d); }; };

  // Attach events
  document.getElementById('search').oninput = debounce(filter, 250);
  document.getElementById('author').oninput = debounce(filter, 250);
  document.getElementById('year').onchange = filter;

  // Run everything
  render();
  setStyle('apa');
  filter();
});
</script>

<hr style="margin:80px 0; border-top:1px solid #eee;">

<p style="text-align:center; color:#555;">
  Automatically synced from 
  <a href="https://orcid.org/0000-0001-9385-1768" target="_blank">ORCID</a> • 
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">Google Scholar</a>
</p>
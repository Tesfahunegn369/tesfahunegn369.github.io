---
layout: default
title: Publications
---

# 연구업적 (Publications)

<div style="text-align:center; margin:40px 0;">
  <input type="text" id="search" placeholder="Search by title…" style="padding:12px 16px; width:280px; margin:5px; border:1px solid #ccc; border-radius:6px;">
  <input type="text" id="author" placeholder="Filter by author…" style="padding:12px 16px; width:280px; margin:5px; border:1px solid #ccc; border-radius:6px;">
  <select id="year-filter" style="padding:12px 16px; margin:5px; border:1px solid #ccc; border-radius:6px;">
    <option value="">All years</option>
  </select>
</div>

<div style="text-align:center; margin-bottom:50px;">
  <button id="apa-btn" class="style-btn active">APA Style</button>
  <button id="ieee-btn" class="style-btn">IEEE Style</button>
</div>

{% assign pubs = site.data.publications %}
{% if pubs == empty %}
  <p style="text-align:center; color:#c00;">No publications found. Check <code>_data/publications.yml</code></p>
{% else %}

  {% assign all = '' | split: '' %}
  {% for year_entry in pubs %}
    {% assign year = year_entry[0] %}
    {% for p in year_entry[1] %}
      {% assign pub = p | merge: { "year": year } %}
      {% assign all = all | push: pub %}
    {% endfor %}
  {% endfor %}

  {% assign sorted = all | sort: 'year' | reverse %}
  {% assign years = sorted | map: 'year' | uniq | sort | reverse %}

  <script>
    const years = {{ years | jsonify }};
    const select = document.getElementById('year-filter');
    years.forEach(y => select.add(new Option(y, y)));
  </script>

  {% for y in years %}
    <h3 style="margin:70px 0 20px; padding-bottom:10px; border-bottom:3px solid #0066cc; font-size:1.9em; color:#222;">
      {{ y }}
    </h3>

    <ol class="pub-list">
      {% assign year_count = 0 %}
      {% for p in sorted %}
        {% if p.year == y %}
          {% assign year_count = year_count | plus: 1 %}
          <li class="pub-item"
              data-title="{{ p.title | escape }}"
              data-authors="{{ p.authors | escape }}"
              data-year="{{ p.year }}"
              data-venue="{{ p.venue | escape }}"
              data-citations="{{ p.citations | default: 0 }}">

            <span class="num">[{{ year_count }}]</span>
            <span class="text"></span>
            <span class="cites"></span>
            <span class="links">
              {% if p.pdf and p.pdf != '' %}
                <a href="{{ p.pdf | relative_url }}" target="_blank">[PDF]</a>
              {% endif %}
              {% if p.doi and p.doi != '' %}
                <a href="{% if p.doi contains 'http' %}{{ p.doi }}{% else %}https://doi.org/{{ p.doi }}{% endif %}" target="_blank">[DOI]</a>
              {% endif %}
              {% if p.bibtex %}
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
  margin: 20px 0;
}
.pub-item {
  list-style: none;
  margin-bottom: 22px;
  display: flex;
  align-items: flex-start;
  line-height: 1.7;
  font-size: 1.02em;
}
.pub-item .num {
  font-weight: bold;
  color: #0066cc;
  min-width: 42px;
  margin-right: 10px;
}
.pub-item .text {
  flex: 1;
}
.pub-item .cites {
  color: #666;
  font-size: 0.92em;
  margin-left: 12px;
  white-space: nowrap;
}
.pub-item .links a {
  color: #0066cc;
  text-decoration: none;
  margin-right: 12px;
  font-size: 0.92em;
}
.pub-item .links a:hover { text-decoration: underline; }

.style-btn {
  padding: 10px 28px;
  margin: 0 8px;
  font-weight: bold;
  border: 2px solid #0066cc;
  background: white;
  color: #0066cc;
  border-radius: 6px;
  cursor: pointer;
}
.style-btn.active {
  background: #0066cc;
  color: white;
}
</style>

<script>
// Run after page fully loads
document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.pub-item');

  function render(style = 'apa') {
    items.forEach(el => {
      const a = el.dataset.authors;
      const y = el.dataset.year;
      const t = el.dataset.title;
      const v = el.dataset.venue;
      const c = el.dataset.citations || '0';

      const text = style === 'apa'
        ? `<strong>${a}</strong> (${y}). <em>${t}</em>. ${v}.`
        : `<strong>${a}</strong>, “${t},” <em>${v}</em>, ${y}.`;

      el.querySelector('.text').innerHTML = text;
      el.querySelector('.cites').textContent = `(${c} citation${c !== '1' ? 's' : ''})`;
    });
  }

  function filter() {
    const sq = document.getElementById('search').value.toLowerCase();
    const aq = document.getElementById('author').value.toLowerCase();
    const yq = document.getElementById('year-filter').value;

    items.forEach(el => {
      const matchTitle = el.dataset.title.toLowerCase().includes(sq);
      const matchAuthor = el.dataset.authors.toLowerCase().includes(aq);
      const matchYear = !yq || el.dataset.year === yq;
      el.style.display = (matchTitle && matchAuthor && matchYear) ? '' : 'none';
    });
  }

  // Button toggle
  document.getElementById('apa-btn').onclick = () => {
    render('apa');
    document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('apa-btn').classList.add('active');
  };
  document.getElementById('ieee-btn').onclick = () => {
    render('ieee');
    document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('ieee-btn').classList.add('active');
  };

  // Search with debounce
  const debounce = (fn, delay) => {
    let t; return () => { clearTimeout(t); t = setTimeout(fn, delay); };
  };
  document.getElementById('search').oninput = debounce(filter, 250);
  document.getElementById('author').oninput = debounce(filter, 250);
  document.getElementById('year-filter').onchange = filter;

  // Initial render
  render('apa');
  filter();
});
</script>

<hr style="margin:90px 0; border-top:1px solid #eee;">

<p style="text-align:center; color:#555; font-size:1.1em;">
  Automatically synced from 
  <a href="https://orcid.org/0000-0001-9385-1768" target="_blank">ORCID</a> • 
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">Google Scholar</a>
</p>
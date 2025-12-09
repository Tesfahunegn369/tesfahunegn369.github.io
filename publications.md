---
layout: default
title: Publication
---

# 연구업적

## Selected Publications (from Google Scholar)
<div class="filters">
  <input id="search" placeholder="Search title…">
  <input id="author" placeholder="Filter author…">
  <select id="year">
    <option value="">All years</option>
    {% for y in site.data.publications %}
    <option value="{{ y[0] }}">{{ y[0] }}</option>
    {% endfor %}
  </select>
</div>

<script>
document.querySelectorAll('.filters input, .filters select')
  .forEach(el => el.oninput = filter);

function filter() {
  const t = search.value.toLowerCase();
  const a = author.value.toLowerCase();
  const y = year.value;

  document.querySelectorAll('.pub-item').forEach(p => {
    const ok =
      p.dataset.title.toLowerCase().includes(t) &&
      p.dataset.authors.toLowerCase().includes(a) &&
      (!y || p.dataset.year === y);
    p.style.display = ok ? '' : 'none';
  });
}

</script>
<div class="format-toggle">
  <button onclick="setStyle('apa')">APA</button>
  <button onclick="setStyle('ieee')">IEEE</button>
</div>

<script>
function setStyle(style){
  document.querySelectorAll('.pub-item').forEach(p=>{
    const a=p.dataset.authors, y=p.dataset.year,
          t=p.dataset.title, v=p.dataset.venue;
    p.querySelector('.pub-text').innerHTML =
      style==='apa'
      ? `${a} (${y}). <i>${t}</i>. ${v}.`
      : `${a}, “${t},” <i>${v}</i>, ${y}.`;
  });
}
document.addEventListener("DOMContentLoaded",()=>setStyle('apa'));
</script>


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

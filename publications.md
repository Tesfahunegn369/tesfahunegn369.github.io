---
layout: default
title: Publications
---

# 연구업적 (Publications)

<div style="text-align:center; margin:40px 0;">
  <input id="search" placeholder="Search title…" style="padding:10px;width:260px;">
  <input id="author" placeholder="Filter author…" style="padding:10px;width:260px;">
  <select id="year" style="padding:10px;">
    <option value="">All years</option>
  </select>
</div>

<div style="text-align:center; margin-bottom:40px;">
  <button onclick="setStyle('apa')" id="btn-apa" class="active">APA</button>
  <button onclick="setStyle('ieee')" id="btn-ieee">IEEE</button>
</div>

<style>
button{padding:8px 18px;border:2px solid #0066cc;background:#fff;color:#0066cc;border-radius:6px}
button.active{background:#0066cc;color:#fff}
.pub-item{margin-bottom:16px}
.pub-links a{margin-left:8px}
.year-header{border-bottom:2px solid #0066cc;margin-top:50px}
</style>

{% assign pubs = site.data.publications %}
{% assign all = "" | split:"" %}

{% for y in pubs %}
  {% for p in y[1] %}
    {% assign pub = p | merge: { "year": y[0] } %}
    {% assign all = all | push: pub %}
  {% endfor %}
{% endfor %}

{% assign sorted = all | sort: "year" | reverse %}
{% assign years = sorted | map: "year" | uniq %}

<script>
  const years = {{ years | jsonify }};
  years.forEach(y => year.add(new Option(y, y)));
</script>

{% for y in years %}
<h3 class="year-header">{{ y }}</h3>
<ol>
  {% assign i = 0 %}
  {% for p in sorted %}
    {% if p.year == y %}
      {% assign i = i | plus:1 %}
      <li class="pub-item"
          data-title="{{ p.title | escape }}"
          data-authors="{{ p.authors | escape }}"
          data-year="{{ p.year }}"
          data-venue="{{ p.venue | escape }}">

        <span class="pub-text">
          <strong>{{ p.authors }}</strong> ({{ p.year }}).
          <em>{{ p.title }}</em>. {{ p.venue }}.
        </span>

        {% if p.citations %}
        <span style="color:#666">({{ p.citations }} citations)</span>
        {% endif %}

        <span class="pub-links">
          {% if p.pdf and p.pdf != "" %}
            <a href="{{ p.pdf | relative_url }}" target="_blank">[PDF]</a>
          {% endif %}
          {% if p.doi and p.doi != "" %}
            <a href="https://doi.org/{{ p.doi }}" target="_blank">[DOI]</a>
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

<script>
function setStyle(style){
  document.querySelectorAll('.pub-item').forEach(el=>{
    const a=el.dataset.authors,
          t=el.dataset.title,
          v=el.dataset.venue,
          y=el.dataset.year;
    el.querySelector('.pub-text').innerHTML =
      style==='apa'
      ? `<strong>${a}</strong> (${y}). <em>${t}</em>. ${v}.`
      : `<strong>${a}</strong>, “${t},” <em>${v}</em>, ${y}.`;
  });
  document.querySelectorAll('button').forEach(b=>b.classList.remove('active'));
  document.getElementById('btn-'+style).classList.add('active');
}

function filter(){
  const s=search.value.toLowerCase(),
        a=author.value.toLowerCase(),
        y=year.value;
  document.querySelectorAll('.pub-item').forEach(el=>{
    el.style.display =
      el.dataset.title.toLowerCase().includes(s) &&
      el.dataset.authors.toLowerCase().includes(a) &&
      (!y || el.dataset.year===y)
      ? '' : 'none';
  });
}

search.oninput=author.oninput=filter;
year.onchange=filter;
setStyle('apa');
</script>

<hr>

<p style="text-align:center">
Synced from
<a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">Google Scholar</a>
</p>

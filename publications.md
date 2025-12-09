---
layout: default
title: Publications
---

# Publications

## Selected Publications (from Google Scholar)

<div class="filters" style="margin: 20px 0; text-align: center;">
  <input id="search" placeholder="Search title…" style="width:200px; padding:8px; margin:5px;">
  <input id="author" placeholder="Filter author…" style="width:200px; padding:8px; margin:5px;">
  <select id="year" style="padding:8px; margin:5px;">
    <option value="">All years</option>
  </select>
</div>

<div class="format-toggle" style="margin-bottom: 20px; text-align: center;">
  <button onclick="setStyle('apa')" class="active">APA</button>
  <button onclick="setStyle('ieee')">IEEE</button>
</div>

<script>
function filter() {
  const term = document.getElementById('search').value.toLowerCase();
  const auth = document.getElementById('author').value.toLowerCase();
  const year = document.getElementById('year').value;

  document.querySelectorAll('.pub-item').forEach(item => {
    const matchesTitle  = item.dataset.title.toLowerCase().includes(term);
    const matchesAuthor = item.dataset.authors.toLowerCase().includes(auth);
    const matchesYear   = !year || item.dataset.year === year;

    item.style.display = (matchesTitle && matchesAuthor && matchesYear) ? '' : 'none';
  });
}

function setStyle(style) {
  document.querySelectorAll('.pub-item').forEach(item => {
    const a = item.dataset.authors;
    const y = item.dataset.year;
    const t = item.dataset.title;
    const v = item.dataset.venue;

    const text = style === 'apa'
      ? `${a} (${y}). <i>${t}</i>. ${v}.`
      : `${a}, "${t}," <i>${v}</i>, ${y}.`;

    item.querySelector('.pub-text').innerHTML = text;
  });

  // update active button style
  document.querySelectorAll('.format-toggle button').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}

// run on load
document.addEventListener
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.filters input, .filters select')
          .forEach(el => el.addEventListener('input', filter));
  setStyle('apa');
});
</script>

{% assign raw_pubs = site.data.publications | default: empty_array %}

{% if raw_pubs == empty %}
  <p><em>No publications data found (check <code>_data/publications.yml</code> or <code>.json</code>).</em></p>
{% else %}

  {% comment %}
    raw_pubs is expected to be an array of hashes with at least:
      title, authors, year, venue, (pdf, doi, bibtex optional)
  {% endcomment %}

  {% assign pubs = raw_pubs | sort: "year" | reverse %}

  {% comment %}Populate the year dropdown{% endcomment %}
  <script>
    const years = [...new Set([{% for p in pubs %}"{{ p.year }}",{% endfor %}])].sort().reverse();
    const select = document.getElementById('year');
    years.forEach(y => {
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      select.appendChild(opt);
    });
  </script>

  {% assign years_group = pubs | map: "year" | uniq | sort | reverse %}

  {% for year in years_group %}
    <h3>{{ year }}</h3>
    <ol class="pub-list">
      {% for p in pubs %}
        {% if p.year == year %}
          <li class="pub-item"
              data-title="{{ p.title | escape }}"
              data-authors="{{ p.authors | escape }}"
              data-year="{{ p.year }}"
              data-venue="{{ p.venue | escape }}">

            <span class="pub-text"></span>

            <span class="pub-links" style="margin-left: 15px; font-size:0.9em;">
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
        {% endif %}
      {% endfor %}
    </ol>
  {% endfor %}

{% endif %}

<p style="margin-top: 40px;">
  For the full and always up-to-date list, visit my
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">
    Google Scholar profile
  </a>.
</p>
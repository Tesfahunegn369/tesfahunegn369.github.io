---
layout: default
title: Publications
---

# Publications

## Selected Publications

<div class="filters" style="margin: 2rem 0; text-align: center;">
  <input type="text" id="search" placeholder="Search title…" style="padding: 10px; width: 220px; margin: 5px;">
  <input type="text" id="author" placeholder="Filter by author…" style="padding: 10px; width: 220px; margin: 5px;">
  <select id="year" style="padding: 10px; margin: 5px;">
    <option value="">All years</option>
  </select>
</div>

<div class="format-toggle" style="text-align: center; margin-bottom: 30px;">
  <button onclick="setStyle('apa')" class="btn-active">APA</button>
  <button onclick="setStyle('ieee')">IEEE</button>
</div>

{% comment %}
  Safely load publications – works whether _data/publications.yml exists or not
{% endcomment %}
{% assign raw_pubs = site.data.publications | default: false %}

{% if raw_pubs == false or raw_pubs == empty %}
  <p><em>No publications data found. Please check <code>_data/publications.yml</code> or <code>_data/publications.json</code>.</em></p>
{% else %}

  {% comment %} Ensure it's an array and has items {% endcomment %}
  {% assign pubs = raw_pubs | where_exp: "item", "item.year != nil" %}

  {% if pubs.size == 0 %}
    <p><em>No valid publications found (missing 'year' field?).</em></p>
  {% else %}

    {% comment %} Sort by year descending {% endcomment %}
    {% assign sorted_pubs = pubs | sort: "year" | reverse %}

    {% comment %} Extract unique years for headings and dropdown {% endcomment %}
    {% assign all_years = sorted_pubs | map: "year" | uniq | sort: "year" | reverse %}

    {% comment %} Populate year dropdown via JavaScript (safe) {% endcomment %}
    <script>
      const years = {{ all_years | jsonify }};
      const select = document.getElementById('year');
      years.forEach(y => {
        const opt = new Option(y, y);
        select.appendChild(opt);
      });
    </script>

    {% for year in all_years %}
      <h3 style="margin-top: 2.5rem; border-bottom: 1px solid #ddd; padding-bottom: 8px;">{{ year }}</h3>
      <ol class="pub-list" style="padding-left: 1.5rem;">
        {% for p in sorted_pubs %}
          {% if p.year == year %}
            <li class="pub-item"
                data-title="{{ p.title | default: '' | escape }}"
                data-authors="{{ p.authors | default: 'Unknown' | escape }}"
                data-year="{{ p.year }}"
                data-venue="{{ p.venue | default: '' | escape }}">

              <span class="pub-text"></span>

              <span class="pub-links" style="margin-left: 20px; font-size: 0.9em; color: #555;">
                {% if p.pdf %}
                  <a href="{{ p.pdf | relative_url }}" target="_blank">[PDF]</a>
                {% endif %}
                {% if p.doi %}
                  <a href="https://doi.org/{{ p.doi }}" target="_blank">[DOI]</a>
                {% elsif p.doi contains 'http %}
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
{% endif %}

<script>
// Filter logic
function filter() {
  const term = document.getElementById('search').value.toLowerCase();
  const auth = document.getElementById('author').value.toLowerCase();
  const year = document.getElementById('year').value;

  document.querySelectorAll('.pub-item').forEach(item => {
    const matchTitle  = item.dataset.title.toLowerCase().includes(term);
    const matchAuthor = item.dataset.authors.toLowerCase().includes(auth);
    const matchYear   = !year || item.dataset.year === year;

    item.style.display = (matchTitle && matchAuthor && matchYear) ? '' : 'none';
  });
}

// Format toggle (APA / IEEE)
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

  // Update active button
  document.querySelectorAll('.format-toggle button').forEach(b => b.classList.remove('btn-active'));
  event.currentTarget.classList.add('btn-active');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Attach filter events
  ['search', 'author', 'year'].forEach(id => {
    document.getElementById(id).addEventListener('input', filter);
  });

  // Default to APA
  setStyle('apa');

  // Initial filter (in case URL has params or something)
  filter();
});
</script>

<style>
.format-toggle button {
  padding: 8px 16px;
  margin: 0 5px;
  border: 1px solid #0077cc;
  background: white;
  color: #0077cc;
  cursor: pointer;
  border-radius: 4px;
}
.format-toggle button.btn-active {
  background: #0077cc;
  color: white;
}
.pub-links a {
  margin-right: 12px;
  text-decoration: none;
  color: #0066aa;
}
.pub-links a:hover {
  text-decoration: underline;
}
</style>

<hr style="margin: 4rem 0;">

<p style="text-align: center; font-size: 1.1em;">
  For the complete and always up-to-date list, visit my<br>
  <a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank" style="font-weight: bold;">
    Google Scholar Profile
  </a>
</p>
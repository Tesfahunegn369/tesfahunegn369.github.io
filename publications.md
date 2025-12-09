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

<div style="text-align:center; margin-bottom:30px;">
  <button onclick="setStyle('apa')" id="btn-apa" class="active">APA Style</button>
  <button onclick="setStyle('ieee')" id="btn-ieee">IEEE Style</button>
</div>

<div style="display:flex; gap:40px; align-items:flex-start; margin-bottom:24px;">
  <div style="flex:1">
    <h3 style="margin:0 0 8px;">Topic Clusters</h3>
    <canvas id="topicChart" width="400" height="200"></canvas>
  </div>
  <div style="flex:2">
    <h3 style="margin:0 0 8px;">Impact Timeline</h3>
    <canvas id="impactAnim" width="800" height="200"></canvas>
  </div>
</div>

<hr style="margin:20px 0;">

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
    <h3 class="year-header" style="margin:40px 0 12px; padding-bottom:8px; border-bottom:3px solid #0066cc;">{{ y }}</h3>
    <ol style="padding-left:0; list-style:none;">
      {% assign count = 0 %}
      {% for p in sorted %}
        {% if p.year == y %}
          {% assign count = count | plus: 1 %}
          <li class="pub-item" style="display:flex; align-items:flex-start; gap:10px; margin-bottom:14px; padding:6px 0;"
              data-title="{{ p.title | escape }}"
              data-authors="{{ p.authors | escape }}"
              data-year="{{ p.year }}"
              data-venue="{{ p.venue | escape }}"
              data-citations="{{ p.citations | default: 0 }}"
              data-bib="{{ p.bibtex | default: '' }}"
              data-doi="{{ p.doi | default: '' }}">
            <div style="min-width:48px; font-weight:bold; color:#0066cc">[{{ count }}]</div>
            <div style="flex:1">
              <div class="pub-text"></div>
              <div class="pub-meta" style="margin-top:6px; color:#666; font-size:0.95em;">
                <span class="pub-cites"></span>
                <span class="pub-venue" style="margin-left:12px;"></span>
                <span class="pub-links" style="margin-left:12px;"></span>
              </div>
              <div class="pub-abstract" style="margin-top:8px; display:none; color:#333; background:#fafafa; padding:10px; border-radius:6px;"></div>
            </div>
          </li>
        {% endif %}
      {% endfor %}
    </ol>
  {% endfor %}
{% endif %}

<!-- BibTeX modal viewer -->
<div id="bibModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.6); align-items:center; justify-content:center; z-index:9999;">
  <div style="background:#fff; width:min(900px,95%); max-height:85vh; overflow:auto; padding:20px; border-radius:8px; position:relative;">
    <button id="bibClose" style="position:absolute; right:14px; top:12px; background:#eee; border:none; padding:6px 10px; cursor:pointer;">Close</button>
    <h3 id="bibTitle"></h3>
    <pre id="bibContent" style="white-space:pre-wrap; word-break:break-word; background:#f7f7f7; padding:12px; border-radius:6px;"></pre>
    <div style="margin-top:12px;">
      <a id="bibDownload" class="download-btn" style="margin-right:12px; color:#0066cc;"></a>
    </div>
  </div>
</div>

<!-- load libs -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-chart-matrix@2.0.1"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script type="text/javascript">
// wrap in DOMContentLoaded to avoid race conditions
document.addEventListener('DOMContentLoaded', () => {
  // populate text and links for each publication
  function renderItems() {
    document.querySelectorAll('.pub-item').forEach(el => {
      const authors = el.dataset.authors;
      const year = el.dataset.year;
      const title = el.dataset.title;
      const venue = el.dataset.venue;
      const cites = el.dataset.citations || "0";
      const doi = el.dataset.doi || "";
      const bib = el.dataset.bib || "";

      el.querySelector('.pub-text').innerHTML =
        `<strong>${authors}</strong> (${year}). <em>${title}</em>. ${venue}.`;

      el.querySelector('.pub-cites').textContent = ` ${cites} citation${cites === '1' ? '' : 's'}`;

      // venue badge
      el.querySelector('.pub-venue').innerHTML = `<span style="background:#eef6ff;color:#0066cc;padding:4px 8px;border-radius:14px;font-weight:600;">${venue}</span>`;

      // links
      const links = el.querySelector('.pub-links');
      links.innerHTML = '';
      if (doi) {
        const doiLink = document.createElement('a');
        doiLink.href = (doi.indexOf('http') === 0) ? doi : `https://doi.org/${doi}`;
        doiLink.target = "_blank";
        doiLink.rel = "noopener";
        doiLink.textContent = "[DOI]";
        links.appendChild(doiLink);

        // Altmetric donut embed (lazy)
        const altWrap = document.createElement('span');
        altWrap.style.marginLeft = '8px';
        altWrap.innerHTML = `<span class="altmetric-embed" data-badge-type="donut" data-doi="${doi}"></span>`;
        links.appendChild(altWrap);

        // Dimensions badge (async script loads once)
        const dim = document.createElement('span');
        dim.innerHTML = `<span class="__dimensions_badge_embed__" data-doi="${doi}"></span>`;
        links.appendChild(dim);
      }

      if (bib) {
        // BibTeX modal open
        const bibA = document.createElement('a');
        bibA.href = `/bibtex/${bib}.bib`;
        bibA.download = `${bib}.bib`;
        bibA.textContent = "[BibTeX]";
        bibA.style.marginLeft = '8px';
        // show modal on click to view
        bibA.addEventListener('click', function(ev){
          ev.preventDefault();
          openBibModal(bib, title);
        });
        links.appendChild(bibA);

        // also add RIS/ENW if present
        const risHref = `/bibtex/${bib}.ris`;
        const enwHref = `/bibtex/${bib}.enw`;
        const risA = document.createElement('a');
        risA.href = risHref;
        risA.download = `${bib}.ris`;
        risA.textContent = "[RIS]";
        risA.style.marginLeft = '8px';
        links.appendChild(risA);

        const enwA = document.createElement('a');
        enwA.href = enwHref;
        enwA.download = `${bib}.enw`;
        enwA.textContent = "[ENW]";
        enwA.style.marginLeft = '8px';
        links.appendChild(enwA);
      }
    });
  }

  // Bib modal functions
  const bibModal = document.getElementById('bibModal');
  const bibTitle = document.getElementById('bibTitle');
  const bibContent = document.getElementById('bibContent');
  const bibDownload = document.getElementById('bibDownload');
  document.getElementById('bibClose').addEventListener('click', ()=>bibModal.style.display='none');

  function openBibModal(bibKey, title) {
    bibTitle.textContent = title;
    bibContent.textContent = "Loading...";
    bibDownload.href = `/bibtex/${bibKey}.bib`;
    bibDownload.textContent = "Download .bib";
    bibDownload.setAttribute("download", `${bibKey}.bib`);
    bibModal.style.display = 'flex';
    fetch(`/bibtex/${bibKey}.bib`).then(r=>{
      if (!r.ok) throw new Error("Not found");
      return r.text();
    }).then(text=>{
      bibContent.textContent = text;
    }).catch(e=>{
      bibContent.textContent = "BibTeX file not available.";
    });
  }

  // Toggle APA/IEEE
  window.setStyle = function(style) {
    document.querySelectorAll('.pub-item').forEach(el => {
      const authors = el.dataset.authors;
      const year = el.dataset.year;
      const title = el.dataset.title;
      const venue = el.dataset.venue;
      const container = el.querySelector('.pub-text');
      container.innerHTML = style === 'apa'
        ? `<strong>${authors}</strong> (${year}). <em>${title}</em>. ${venue}.`
        : `<strong>${authors}</strong>, “${title},” <em>${venue}</em>, ${year}.`;
    });
    document.getElementById('btn-apa').classList.toggle('active', style==='apa');
    document.getElementById('btn-ieee').classList.toggle('active', style!=='apa');
  };

  // Collapsible abstracts: fetch via CrossRef or semantic APIs if available (light fallback)
  // For now create toggles that fetch CrossRef abstract if DOI exists
  function setupAbstractToggles() {
    document.querySelectorAll('.pub-item').forEach(el=>{
      const doi = el.dataset.doi;
      const absWrap = el.querySelector('.pub-abstract');
      if (!doi) return;
      const btn = document.createElement('button');
      btn.textContent = "Show abstract";
      btn.style.marginLeft = '8px';
      btn.style.padding = '6px 8px';
      btn.style.cursor = 'pointer';
      btn.addEventListener('click', async () => {
        if (absWrap.style.display === 'block') {
          absWrap.style.display = 'none';
          btn.textContent = "Show abstract";
          return;
        }
        btn.textContent = "Loading...";
        try {
          const resp = await fetch(`https://api.crossref.org/works?query.bibliographic=${encodeURIComponent(el.dataset.title)}`);
          const js = await resp.json();
          const item = js.message.items && js.message.items[0];
          const abstract = item && item.abstract ? (item.abstract.replace(/<\/?jats:[^>]+>/g,'').replace(/<\/?[^>]+>/g,'')) : "Abstract not available.";
          absWrap.textContent = abstract;
        } catch (e) {
          absWrap.textContent = "Abstract not available.";
        } finally {
          absWrap.style.display = 'block';
          btn.textContent = "Hide abstract";
        }
      });
      el.querySelector('.pub-meta').appendChild(btn);
    });
  }

  // Search/filter
  function filter() {
    const sq = document.getElementById('search').value.toLowerCase();
    const aq = document.getElementById('author').value.toLowerCase();
    const yq = document.getElementById('year').value;
    document.querySelectorAll('.pub-item').forEach(el => {
      const matchTitle = el.dataset.title.toLowerCase().includes(sq);
      const matchAuthor = el.dataset.authors.toLowerCase().includes(aq);
      const matchYear = !yq || el.dataset.year === yq;
      el.style.display = (matchTitle && matchAuthor && matchYear) ? '' : 'none';
    });
  }
  const debounce = (fn, ms) => { let t; return (...a)=>{clearTimeout(t); t=setTimeout(()=>fn(...a), ms);} };
  document.getElementById('search').oninput = debounce(filter, 200);
  document.getElementById('author').oninput = debounce(filter, 200);
  document.getElementById('year').onchange = filter;

  // Topic clusters chart (client-side) - reads assets/data/topic_clusters.json
  fetch('/assets/data/topic_clusters.json').then(r=>r.json()).then(data=>{
    const ctx = document.getElementById('topicChart').getContext('2d');
    const labels = Object.keys(data);
    const values = Object.values(data);
    new Chart(ctx, {
      type: 'pie',
      data: { labels, datasets: [{ data: values }] },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
    });
  }).catch(()=>{ /* silent */ });

  // Animated impact timeline: reads assets/data/impact_timeline.json
  fetch('/assets/data/impact_timeline.json').then(r=>r.json()).then(data=>{
    const ctx = document.getElementById('impactAnim').getContext('2d');
    const labels = Object.keys(data);
    const values = Object.values(data);
    new Chart(ctx, {
      type: 'line',
      data: { labels, datasets: [{ label:'Papers', data: values, tension:0.3, fill:true }] },
      options: { animation:{duration:1800}, scales:{y:{beginAtZero:true}} }
    });
  }).catch(()=>{ /* silent */ });

  // load altmetric + dimensions widgets (only once)
  (function loadBadges(){
    if (!document.querySelector('script[src="//d1bxh8uas1mnw7.cloudfront.net/assets/embed.js"]')) {
      const s = document.createElement('script');
      s.src = '//d1bxh8uas1mnw7.cloudfront.net/assets/embed.js';
      document.body.appendChild(s);
    }
    if (!document.querySelector('script[src="https://badge.dimensions.ai/badge.js"]')) {
      const s2 = document.createElement('script');
      s2.src = 'https://badge.dimensions.ai/badge.js';
      s2.async = true;
      document.body.appendChild(s2);
    }
  })();

  // initial render
  renderItems();
  setupAbstractToggles();
  setStyle('apa');
  filter();
});
</script>

<style>
/* minor styling for modal download link */
.download-btn { color:#0066cc; text-decoration:none; font-weight:bold; }
</style>

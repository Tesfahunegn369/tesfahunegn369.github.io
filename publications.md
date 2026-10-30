---
layout: default
title: Publications
---

# 연구업적 (Publications)

<style>
.pub-list{list-style:none;padding:0}
.pub-item{margin:18px 0;padding-left:10px;border-left:3px solid #0066cc}
.pub-title{font-weight:600}
.venue{background:#eef;padding:2px 8px;border-radius:12px;font-size:.85em;margin-left:6px}
.cite-bar{height:6px;background:#ddd;border-radius:4px;overflow:hidden;margin:6px 0}
.cite-fill{height:100%;background:#0066cc}
.links a{margin-left:10px;font-size:.9em}
.abstract{display:none;margin-top:8px;color:#444}
.orcid{margin-left:6px}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.6)}
.modal-content{background:#fff;padding:20px;margin:10% auto;width:70%;border-radius:8px}
</style>

{% assign pubs = site.data.publications %}
{% assign all = "" | split:"" %}

{% for y in pubs %}
  {% for p in y[1] %}
    {% assign pub = p | merge:{ "year": y[0] } %}
    {% assign all = all | push: pub %}
  {% endfor %}
{% endfor %}

{% assign sorted = all | sort: "year" | reverse %}
{% assign years = sorted | map:"year" | uniq %}

{% for y in years %}
<h3 style="margin:70px 0 20px;border-bottom:3px solid #0066cc">{{ y }}</h3>
<ol class="pub-list">

{% assign i = 0 %}
{% for p in sorted %}
{% if p.year == y %}
{% assign i = i | plus:1 %}

<li class="pub-item">
  <span class="num">[{{ i }}]</span>

  <div class="pub-title">
    <strong>{{ p.authors }}</strong>
    {% if p.orcid %}
      <a href="https://orcid.org/{{ p.orcid }}" target="_blank" class="orcid">🆔</a>
    {% endif %}
    ({{ p.year }}).
    <em>{{ p.title }}</em>.
    <span class="venue">{{ p.venue }}</span>
  </div>

  {% if p.citations %}
  <div class="cite-bar">
    <div class="cite-fill" style="width:{{ p.citations | times:3 | at_most:100 }}%"></div>
  </div>
  <small>{{ p.citations }} citations</small>
  {% endif %}

  <div class="links">
    {% if p.pdf and p.pdf != "" %}
      <a href="{{ p.pdf | relative_url }}" target="_blank">[PDF]</a>
    {% endif %}
    {% if p.doi %}
      <a href="https://doi.org/{{ p.doi }}" target="_blank">[DOI]</a>
    {% endif %}
    {% if p.bibtex %}
      <a href="#" onclick="showBib('{{ p.bibtex }}')">[BibTeX]</a>
    {% endif %}
    {% if p.abstract %}
      <a href="#" onclick="toggleAbs(this)">[Abstract]</a>
    {% endif %}
  </div>

  {% if p.abstract %}
  <div class="abstract">
    {{ p.abstract }}
  </div>
  {% endif %}
</li>

{% endif %}
{% endfor %}
</ol>
{% endfor %}

<!-- BibTeX Modal -->
<div id="bibModal" class="modal" onclick="this.style.display='none'">
  <div class="modal-content">
    <pre id="bibContent"></pre>
  </div>
</div>

<script>
function toggleAbs(el){
  el.parentElement.nextElementSibling.classList.toggle('show');
  el.parentElement.nextElementSibling.style.display =
    el.parentElement.nextElementSibling.style.display === 'block' ? 'none' : 'block';
}
function showBib(key){
  fetch(`/bibtex/${key}.bib`)
    .then(r=>r.text())
    .then(t=>{
      bibContent.textContent=t;
      bibModal.style.display='block';
    });
}
</script>

<hr>
<p style="text-align:center">
Synced from
<a href="https://orcid.org/0000-0001-9385-1768" target="_blank">ORCID</a> •
<a href="https://scholar.google.com/citations?user=qgSlPxcAAAAJ" target="_blank">Google Scholar</a>
</p>

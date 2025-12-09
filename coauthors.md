---
layout: default
title: Co-author
---

<h1 id="coauthor-name" style="margin-bottom:10px;"></h1>
<p id="coauthor-meta" style="color:#555;"></p>

<canvas id="citationTrend" height="120" style="margin:40px 0;"></canvas>

<h2 style="margin-top:50px;">Publications</h2>
<ol id="papers" style="padding-left:0;"></ol>

<style>
.pub-item { margin-bottom:20px; line-height:1.7; }
.pub-title { font-weight:bold; }
.pub-venue { background:#eef; color:#003366; padding:3px 8px; border-radius:6px; font-size:.85em; margin-left:6px; }
.abstract { display:none; margin:8px 0 0 28px; color:#444; }
.toggle { cursor:pointer; color:#0066cc; font-size:.9em; margin-left:8px; }
</style>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
// ============================
// SAFE BOOTSTRAP (no race)
// ============================
document.addEventListener("DOMContentLoaded", () => {

  // ---------- CONFIG ----------
  const PUBLICATIONS = {{ site.data.publications | jsonify }};
  
  // ---------- UTIL ----------
  const slug = location.pathname.split('/').pop();
  const authorName = slug.replace(/-/g,' ').toUpperCase();

  document.getElementById("coauthor-name").textContent = authorName;
  document.getElementById("coauthor-meta").textContent =
    "Automatically generated co-author profile";

  // ---------- COLLECT PAPERS ----------
  let papers = [];
  Object.values(PUBLICATIONS).forEach(yearList=>{
    yearList.forEach(p=>{
      if(p.authors.toLowerCase().replace(/;/g,'').includes(slug.replace(/-/g,''))){
        papers.push(p);
      }
    });
  });

  if(!papers.length){
    document.getElementById("papers").innerHTML =
      "<li>No publications found.</li>";
    return;
  }

  // ---------- AUTO ABSTRACT ----------
  const makeAbstract = (t,v) =>
    `This work investigates ${t.toLowerCase()}, published in ${v}. 
     The study focuses on methodology, experimentation, and system-level insights.`;

  // ---------- RENDER PAPERS ----------
  const citationByYear = {};
  const list = document.getElementById("papers");

  papers.forEach((p,i)=>{
    citationByYear[p.year] = (citationByYear[p.year]||0) + (p.citations||0);

    const li = document.createElement("li");
    li.className = "pub-item";
    li.innerHTML = `
      <span>[${i+1}]</span>
      <span class="pub-title">${p.title}</span>
      <span class="pub-venue">${p.venue}</span>
      <span class="toggle" data-i="${i}">[abstract]</span>
      <div class="abstract" id="abs-${i}">
        ${p.abstract || makeAbstract(p.title, p.venue)}
      </div>
    `;
    list.appendChild(li);
  });

  // ---------- ABSTRACT TOGGLE ----------
  document.querySelectorAll(".toggle").forEach(t=>{
    t.onclick = ()=>{
      const a = document.getElementById("abs-"+t.dataset.i);
      a.style.display = a.style.display==="block" ? "none":"block";
    };
  });

  // ---------- CITATION CHART ----------
  new Chart(document.getElementById("citationTrend"),{
    type:'bar',
    data:{
      labels:Object.keys(citationByYear),
      datasets:[{
        label:"Citations per year",
        data:Object.values(citationByYear)
      }]
    },
    options:{
      responsive:true,
      plugins:{ legend:{ display:false } }
    }
  });
});
</script>

<hr style="margin:80px 0;">

<p style="text-align:center; color:#666;">
  Back to <a href="/publications">Publications</a>
</p>

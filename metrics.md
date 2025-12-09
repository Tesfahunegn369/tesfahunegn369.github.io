---
title: Metrics
layout: default
---

## Publication Metrics

<div id="metrics">Loading…</div>

<canvas id="heatmap" width="800" height="400"></canvas>
<canvas id="topics" width="600" height="400"></canvas>
<canvas id="impact" width="800" height="400"></canvas>

<canvas id="citationChart" style="max-width:900px"></canvas>

<h2>Co-author Network</h2>
<div id="coauthors"></div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>

<script>

// Metrics + citation graph
fetch('/assets/data/metrics.json')
  .then(r => r.json())
  .then(d => {
    document.getElementById('metrics').innerHTML =
      `<b>Citations:</b> ${d.citations} |
       <b>h-index:</b> ${d.h_index} |
       <b>i10-index:</b> ${d.i10_index}`;

    new Chart(document.getElementById('citationChart'), {
      type: 'line',
      data: {
        labels: Object.keys(d.cited_by_year),
        datasets: [{
          label: 'Citations per year',
          data: Object.values(d.cited_by_year),
          fill: false,
          borderWidth: 2
        }]
      }
    });
  });

// Co-author network
d3.json('/assets/data/coauthors.json').then(data => {
  const svg = d3.select("#coauthors")
    .append("svg")
    .attr("width", 800)
    .attr("height", 500);

  const sim = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d=>d.id).distance(120))
    .force("charge", d3.forceManyBody().strength(-250))
    .force("center", d3.forceCenter(400,250));

  const link = svg.selectAll("line")
    .data(data.links)
    .enter().append("line")
    .attr("stroke","#bbb");

  const node = svg.selectAll("circle")
    .data(data.nodes)
    .enter().append("circle")
    .attr("r",6)
    .attr("fill","#0077cc");

  sim.on("tick",()=>{
    link.attr("x1",d=>d.source.x)
        .attr("y1",d=>d.source.y)
        .attr("x2",d=>d.target.x)
        .attr("y2",d=>d.target.y);
    node.attr("cx",d=>d.x)
        .attr("cy",d=>d.y);
  });
});
</script>


<script>
// ------------------
// Heatmap
// ------------------
fetch('/assets/data/coauthor_heatmap.json').then(r=>r.json()).then(d=>{
  const ctx=document.getElementById('heatmap').getContext('2d');
  const authors=d.authors;
  const values=[];
  authors.forEach(a=>{
    authors.forEach(b=>{
      values.push(d.matrix[a]?.[b]||0);
    });
  });

  new Chart(ctx,{
    type:'matrix',
    data:{datasets:[{
      label:'Co-author Intensity',
      data:values.map((v,i)=>({
        x:i%authors.length,
        y:Math.floor(i/authors.length),
        v:v
      })),
    }]}
  });
});

// ------------------
// Topics
// ------------------
fetch('/assets/data/topic_clusters.json').then(r=>r.json()).then(d=>{
  new Chart(document.getElementById('topics'),{
    type:'pie',
    data:{
      labels:Object.keys(d),
      datasets:[{data:Object.values(d)}]
    }
  });
});

// ------------------
// Impact timeline
// ------------------
fetch('/assets/data/impact_timeline.json').then(r=>r.json()).then(d=>{
  new Chart(document.getElementById('impact'),{
    type:'line',
    data:{
      labels:Object.keys(d),
      datasets:[{
        label:'Publications per year',
        data:Object.values(d),
        tension:0.3
      }]
    },
    options:{animation:{duration:2000}}
  });
});
</script>

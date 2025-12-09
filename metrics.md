---
title: Metrics
layout: default
---

## Publication Metrics

<div id="metrics">Loading...</div>

<canvas id="citationChart" style="max-width:900px"></canvas>
<canvas id="heatmap" width="800" height="400"></canvas>
<canvas id="topics" width="600" height="400"></canvas>
<canvas id="impact" width="800" height="400"></canvas>

<h2>Co-author Network</h2>
<div id="coauthors"></div>

<!-- ✅ Load libraries ONCE (correct order) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-chart-matrix@2.0.1"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>

{% raw %}
<script>
// =====================
// Metrics + Citations
// =====================
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
          borderWidth: 2
        }]
      }
    });
  });

// =====================
// Co-author Network (D3)
// =====================
d3.json('/assets/data/coauthors.json').then(data => {
  const svg = d3.select("#coauthors")
    .append("svg")
    .attr("width", 800)
    .attr("height", 500);

  const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d => d.id).distance(120))
    .force("charge", d3.forceManyBody().strength(-250))
    .force("center", d3.forceCenter(400, 250));

  const link = svg.selectAll("line")
    .data(data.links)
    .enter()
    .append("line")
    .attr("stroke", "#bbb");

  const node = svg.selectAll("circle")
    .data(data.nodes)
    .enter()
    .append("circle")
    .attr("r", 6)
    .attr("fill", "#0077cc");

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
  });
});

// =====================
// Co-author Heatmap
// =====================
fetch('/assets/data/coauthor_heatmap.json')
  .then(r => r.json())
  .then(d => {
    const authors = d.authors;
    const cells = [];

    authors.forEach((a, y) => {
      authors.forEach((b, x) => {
        cells.push({ x, y, v: d.matrix[a]?.[b] || 0 });
      });
    });

    new Chart(document.getElementById('heatmap'), {
      type: 'matrix',
      data: {
        datasets: [{
          label: 'Co-author Intensity',
          data: cells,
          backgroundColor: c =>
            c.raw.v === 0
              ? 'rgba(0,0,0,0)'
              : `rgba(0,119,204,${0.2 + c.raw.v * 0.15})`,
          width: ({ chart }) =>
            chart.chartArea.width / authors.length - 2,
          height: ({ chart }) =>
            chart.chartArea.height / authors.length - 2
        }]
      },
      options: {
        scales: {
          x: { type: 'category', labels: authors },
          y: { type: 'category', labels: authors }
        }
      }
    });
  });

// =====================
// Topic Clusters
// =====================
fetch('/assets/data/topic_clusters.json')
  .then(r => r.json())
  .then(d => {
    new Chart(document.getElementById('topics'), {
      type: 'pie',
      data: {
        labels: Object.keys(d),
        datasets: [{ data: Object.values(d) }]
      }
    });
  });

// =====================
// Impact Timeline
// =====================
fetch('/assets/data/impact_timeline.json')
  .then(r => r.json())
  .then(d => {
    new Chart(document.getElementById('impact'), {
      type: 'line',
      data: {
        labels: Object.keys(d),
        datasets: [{
          label: 'Publications per year',
          data: Object.values(d),
          tension: 0.3
        }]
      },
      options: {
        animation: { duration: 2000 }
      }
    });
  });
</script>
{% endraw %}

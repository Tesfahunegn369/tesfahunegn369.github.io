---
title: Metrics
layout: default
---

## Publication Metrics

<div id="metrics">Loading...</div>
<canvas id="citationChart" style="max-width:900px; margin: 20px auto; display: block;"></canvas>

<canvas id="heatmap" width="800" height="400"></canvas>
<canvas id="topics" width="600" height="400"></canvas>
<canvas id="impact" width="800" height="400"></canvas>

<h2>Co-author Network</h2>
<div id="coauthors" style="text-align:center;"></div>

<!-- Load libraries once, in correct order -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-chart-matrix@2.0.1"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>

{% raw %}
<script>
// =====================
// 1. Citations + h-index
// =====================
fetch('/assets/data/metrics.json')
  .then(r => r.json())
  .then(d => {
    document.getElementById('metrics').innerHTML = `
      <b>Citations:</b> ${d.citations} |
      <b>h-index:</b> ${d.h_index} |
      <b>i10-index:</b> ${d.i10_index}
    `;

    new Chart(document.getElementById('citationChart'), {
      type: 'line',
      data: {
        labels: Object.keys(d.cited_by_year),
        datasets: [{
          label: 'Citations per year',
          data: Object.values(d.cited_by_year),
          borderColor: '#0077cc',
          backgroundColor: 'rgba(0,119,204,0.1)',
          borderWidth: 2,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  });

// =====================
// 2. Co-author Network (D3)
// =====================
d3.json('/assets/data/coauthors.json').then(data => {
  const width = 800;
  const height = 500;

  const svg = d3.select("#coauthors")
    .append("svg")
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;");

  const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svg.append("g")
    .selectAll("line")
    .data(data.links)
    .enter().append("line")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .attr("stroke-width", d => Math.sqrt(d.value || 1));

  const node = svg.append("g")
    .selectAll("circle")
    .data(data.nodes)
    .enter().append("circle")
    .attr("r", d => 5 + (d.weight || 0))
    .attr("fill", "#0077cc")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5);

  node.append("title").text(d => d.id);

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
// 3. Co-author Heatmap
// =====================
fetch('/assets/data/coauthor_heatmap.json')
  .then(r => r.json())
  .then(d => {
    const authors = d.authors;
    const cells = [];

    authors.forEach((a, i) => {
      authors.forEach((b, j) => {
        cells.push({ x: j, y: i, v: (d.matrix[a] && d.matrix[a][b]) || 0 });
      });
    });

    new Chart(document.getElementById('heatmap'), {
      type: 'matrix',
      data: {
        datasets: [{
          label: 'Co-author Intensity',
          data: cells,
          backgroundColor(c) {
            const v = c.raw.v;
            return v === 0 ? 'rgba(0,0,0,0)' : `rgba(0,119,204,${0.2 + v * 0.15})`;
          },
          borderColor: 'rgba(0,0,0,0.1)',
          borderWidth: 1,
          width: ({chart}) => (chart.chartArea?.width || 800) / authors.length - 1,
          height: ({chart}) => (chart.chartArea?.height || 400) / authors.length - 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { type: 'category', labels: authors, ticks: { autoSkip: false, maxRotation: 90, minRotation: 90 } },
          y: { type: 'category', labels: authors }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: ctx => `${authors[ctx[0].dataIndex.x]} × ${authors[ctx[0].dataIndex.y]}`,
              label: ctx => `Papers together: ${ctx.raw.v}`
            }
          }
        }
      }
    });
  });

// =====================
// 4. Topic Clusters (Pie)
// =====================
fetch('/assets/data/topic_clusters.json')
  .then(r => r.json())
  .then(d => {
    const labels = Object.keys(d);
    const values = Object.values(d);

    new Chart(document.getElementById('topics'), {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: [
            '#0077cc', '#ff6384', '#36a2eb', '#ffce56', '#4bc0c0',
            '#9966ff', '#ff9f40', '#c9cbcf', '#ffcd56', '#66bb6a'
          ]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'right' }
        }
      }
    });
  });

// =====================
// 5. Impact Timeline (Publications per year)
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
          borderColor: '#0077cc',
          backgroundColor: 'rgba(0,119,204,0.1)',
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        animation: { duration: 2000 }
      }
    });
  });
</script>
{% endraw %}
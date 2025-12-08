---
title: Metrics
layout: default
---

## Publication Metrics

<div id="metrics">
Loading metrics...
</div>

<canvas id="citationChart" style="max-width:900px"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
fetch('/assets/data/metrics.json').then(r=>r.json()).then(d=>{
  document.getElementById('metrics').innerHTML = `<strong>Citations:</strong> ${d.citations} &nbsp; <strong>h-index:</strong> ${d.h_index} &nbsp; <strong>i10-index:</strong> ${d.i10_index}`;
  const labels = Object.keys(d.cited_by_year);
  const values = Object.values(d.cited_by_year);
  new Chart(document.getElementById('citationChart'), {
    type: 'line',
    data: { labels: labels, datasets:[{label:'Citations per year', data:values, fill:false, borderWidth:2}] }
  });
});
</script>

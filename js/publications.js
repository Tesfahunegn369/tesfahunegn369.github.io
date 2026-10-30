(() => {
  const list = document.getElementById('publication-list');
  const status = document.getElementById('publication-status');
  if (!list || !status) return;
  const safeUrl = (value) => {
    if (!value || !String(value).trim()) return '';
    try { const u = new URL(value, window.location.href); return ['http:', 'https:'].includes(u.protocol) ? u.href : ''; }
    catch { return ''; }
  };
  function render(data) {
    const publications = Array.isArray(data.publications) ? data.publications.slice() : [];
    publications.sort((a,b) => (Number(b.year)||0) - (Number(a.year)||0) || String(a.title||'').localeCompare(String(b.title||'')));
    if (!publications.length) {
      status.textContent = 'The automatic publication sync has not populated this list yet. You can view the current record on Google Scholar using the link below.';
      return;
    }
    status.textContent = `Loaded ${publications.length} publication${publications.length === 1 ? '' : 's'}${data.updated_at ? ` · Last updated ${data.updated_at}` : ''}${data.source ? ` · Source: ${data.source}` : ''}.`;
    let currentYear = null;
    for (const p of publications) {
      const year = String(p.year || 'Year not listed');
      if (year !== currentYear) {
        const heading = document.createElement('h3');
        heading.className = 'publication-year'; heading.textContent = year;
        list.appendChild(heading); currentYear = year;
      }
      const article = document.createElement('article'); article.className = 'publication';
      const title = document.createElement('h3');
      const titleUrl = safeUrl(p.url || p.scholar_url || p.doi_url);
      if (titleUrl) { const a = document.createElement('a'); a.href = titleUrl; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = p.title || 'Untitled publication'; title.appendChild(a); }
      else title.textContent = p.title || 'Untitled publication';
      article.appendChild(title);
      if (p.authors) { const authors = document.createElement('p'); authors.textContent = p.authors; article.appendChild(authors); }
      const venue = [p.venue, p.volume, p.pages].filter(Boolean).join(', ');
      if (venue) { const meta = document.createElement('p'); meta.className = 'entry-place'; meta.textContent = venue; article.appendChild(meta); }
      const details = [];
      if (p.citations !== null && p.citations !== undefined && p.citations !== '') details.push(`Citations: ${p.citations}`);
      if (p.doi) details.push(`DOI: ${p.doi}`);
      if (details.length) { const detail = document.createElement('p'); detail.className = 'small-note'; detail.textContent = details.join(' · '); article.appendChild(detail); }
      const links = document.createElement('div'); links.className = 'text-links';
      const candidates = [[p.url, 'Paper'], [p.pdf_url, 'PDF'], [p.doi_url || (p.doi ? `https://doi.org/${p.doi}` : ''), 'DOI'], [p.scholar_url, 'Google Scholar']];
      candidates.forEach(([url,label]) => { const href = safeUrl(url); if (href) { const a = document.createElement('a'); a.href = href; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = label; links.appendChild(a); } });
      if (links.childElementCount) article.appendChild(links);
      list.appendChild(article);
    }
  }
  fetch(`publications.json?v=${Date.now()}`, {cache: 'no-store'})
    .then(response => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); })
    .then(render)
    .catch(() => { status.textContent = 'Publication data could not be loaded (if you opened this file directly from disk, run a local server such as "python -m http.server"). Please visit the Google Scholar profile linked below.'; });
})();

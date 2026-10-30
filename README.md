# Academic website: Tesfahunegn Minwuyelet Mengistu

Responsive, dependency-free static academic site for GitHub Pages
(<https://tesfahunegn369.github.io/>). Publications are loaded from `publications.json`,
which a weekly GitHub Actions job refreshes from Google Scholar (with an OpenAlex/ORCID fallback).

## What is on the site

About · Research (interests + featured papers) · Education (with certifications) · Experience ·
Publications (+ conference presentations) · Scholarships & Awards · Leadership & Memberships ·
News · Contact. A Google Translate language selector (English, Amharic and Korean pinned first)
and a JSON-LD `Person` record for search engines are included.

Content was compiled from the profiles linked on the site: Google Scholar, ORCID, ResearchGate,
LinkedIn, Scilit, Global Scholarships, Earth Charter, CIS-PNU Lab, the EurekAlert release and the PNU news pages.

## Repository layout

```
index.html                       main page
404.html, robots.txt, sitemap.xml
css/style.css   js/script.js   js/publications.js
assets/favicon.svg   assets/profile-placeholder.svg   (add assets/profile.jpg)
publications.json                publication data (curated + auto-refreshed)
scripts/update_publications.py   updater used by the workflow
.github/workflows/update-publications.yml
.nojekyll
```

## Deploy

1. Upload the **contents** of this folder to the root of
   <https://github.com/Tesfahunegn369/tesfahunegn369.github.io> (keep the hidden `.github` and `.nojekyll`).
2. **Settings → Pages**: deploy from branch `main`, folder `/ (root)`.
3. **Settings → Actions → General → Workflow permissions**: choose *Read and write permissions*.
4. **Actions → Update publications → Run workflow** to test it. It then runs every Monday at 05:17 UTC.

## Profile photo

Save a portrait as `assets/profile.jpg` (about 420×480 px, under 200 KB). The page uses it automatically
and falls back to the monogram placeholder when the file is missing.

## Publications: how updates work

* `scripts/update_publications.py` tries Google Scholar (ID `qgSlPxcAAAAJ`) via `scholarly`, then OpenAlex (ORCID `0000-0001-9385-1768`).
* Results are **merged** with the records already in `publications.json`: your curated authors, venue, DOI and links are kept,
  citation counts are refreshed, new papers are added, and curated papers that a source misses are not deleted.
* To remove a paper permanently, delete it from `publications.json`. To add one by hand, copy an existing record.
* If both sources fail, the last good file is kept.
* Google Scholar may block cloud runners; that is expected and handled by the fallback.

Local test: `pip install requests scholarly && python scripts/update_publications.py`, then
`python -m http.server` and open <http://localhost:8000> (opening `index.html` directly from disk blocks `fetch`).

## Things to verify before publishing

* **Institutional email.** The site lists `tesfahun@pusan.ac.kr`. PNU's news page for the PHY-layer survey lists `tesfahunegn9@pusan.ac.kr`. Keep whichever is correct.
* **Degree titles.** Global Scholarships says *MSc in Software Engineering* and *BSc in Computer Science*; EurekAlert and Earth Charter say *Computer Science and Software Engineering* for both. The site follows the first.
* **Dates.** Vice Dean 2021–2023 and Acting Dean Jun–Aug 2023 follow your Global Scholarships and Earth Charter pages.
* No CV file was supplied. Add `cv.pdf` and a link in the hero if you want one.
* Machine translation is by Google Translate and may be unavailable if a browser or network blocks it.

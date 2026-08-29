# Shen Lab · Cardiovascular Precision Medicine

Private, members-only website for the Cardiovascular Precision Medicine Lab (Shen Lab) at Washington University School of Medicine.

- Repository: https://github.com/ProMedGen/shen-lab
- Site (org members, after GitHub login): https://super-adventure-gwynznl.pages.github.io/
- Pages settings: https://github.com/ProMedGen/shen-lab/settings/pages

Led by **Mengcheng Shen, PhD**, Assistant Professor of Medicine and of Developmental Biology.

## The HTML is generated — do not edit `.html` files

Every page (`index.html`, `research.html`, … , `404.html`) plus `robots.txt` and
`sitemap.xml` is written by `scripts/build_pages.py`. Editing a `.html` file
directly works until the next build silently reverts it, so make the change in
the generator and rebuild:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_pages.py
```

The deploy workflow re-runs the generator and fails if the committed HTML does
not match, which is what stops a hand edit from shipping and then vanishing.

Content that changes often lives in `data/`:

- `data/publications.json` — one entry per paper, refreshed by `scripts/fetch_pubmed.py`
- `data/news.json` — news items, newest first by `date`

Prose, page structure, and CSS class names live in the templates at the top of
`scripts/build_pages.py`.

## Build steps

| Script | Purpose | Needs |
| --- | --- | --- |
| `scripts/build_pages.py` | Render all HTML, `robots.txt`, `sitemap.xml` | pillow, ffprobe |
| `scripts/fetch_pubmed.py` | Refresh `data/publications.json` from PubMed | network |
| `scripts/optimize_assets.py` | Re-export web images/videos from source materials | pillow, numpy, ffmpeg |
| `scripts/make_posters.py` | Poster frame for each clip in `assets/video` | pillow, ffmpeg |
| `scripts/verify_site.py` | Browser checks: broken images, page-weight budgets, anchor offsets, mobile menu | playwright |

`build_pages.py` reads the real pixel dimensions of every image and clip so it
can emit `width`/`height` (no layout shift) and size each media well to its own
aspect ratio (no letterboxing). It fails loudly rather than guessing if pillow
or `ffprobe` is unavailable.

## Local preview

```bash
python3 -m http.server 4173
```

Then open `http://127.0.0.1:4173`. To run the browser checks against it:

```bash
.venv/bin/playwright install chromium   # first time only
.venv/bin/python scripts/verify_site.py
```

## Publish

The site is static HTML. GitHub Actions deploys it to GitHub Pages.

1. Repository visibility: **private**
2. Settings → Pages → Source: **GitHub Actions**
3. Settings → Pages → Visibility: **Private** (members with read access)

Private Pages are served on a unique `*.pages.github.io` subdomain, not on
`promedgen.github.io/shen-lab`.

## Going public

The site is currently hidden from search engines on purpose: `PUBLIC = False` in
`scripts/build_pages.py` emits `noindex, nofollow` on every page and a
`Disallow: /` robots.txt, matching the private Pages deployment.

To launch:

1. Settings → Pages → Visibility: **Public**
2. In `scripts/build_pages.py`, set `PUBLIC = True` and set `SITE_URL` to the
   final hostname (a custom domain such as `https://shenlab.wustl.edu` if one is
   registered, otherwise the public Pages URL). `SITE_URL` feeds the canonical
   tags, the social-preview image URL, and `sitemap.xml`.
3. Rebuild and commit, then confirm `robots.txt` reads `Allow: /` and each page
   reports `index, follow`.
4. Submit `sitemap.xml` in Google Search Console.
5. Ask WashU Cardiology to link the site from the
   [faculty page](https://cardiology.wustl.edu/people/mengcheng-shen-phd/) —
   an inbound link from `wustl.edu` does more for discoverability than anything
   on-page.

## Source materials

Lab photographs, movies, and the research-focus document live locally in
`Shen Lab WashU_lab_website_materials/` and are not committed. Web-sized copies
are in `assets/`.

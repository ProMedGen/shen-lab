# Banner / masthead quality plan

## Hard constraint

**Never forge biology.** Real fluorescence / brightfield lab images used as
banners may only be *faithfully upscaled* (Lanczos / Real-ESRGAN class).
Firefly generative models must **not** redraw cell structures for those
assets — that would invent non-biological content.

Firefly is reserved for:
- **News / media** — imaginative illustrative banner (not a data figure)
- **People / team** — cartoon or 素描 group portrait (identity-anchored)

## Current masthead map (problems)

| Page | Asset | Size | Issue |
|---|---|---|---|
| Home hero | `cm-ctnt.jpg` | 1329×995 | soft when full-bleed |
| Research | `cm-ctnt.jpg` | same | **duplicate of home** |
| Models | `vessel-organoid.jpg` | 1400×1406 | soft |
| Publications | `pericytes.jpg` | 1080×808 | soft |
| News | `lab-space.jpg` | 1280×720 | soft; **wrong vibe** for news; **dup with People** |
| People | `lab-space.jpg` | same | soft; wants cartoon team |
| Join | `tissue-culture.jpg` | 1280×720 | soft; too similar to People |
| Contact | `smc-myh11.jpg` | 720×721 | very soft |
| 404 | `epicardial.jpg` | 727×702 | soft |

## Target assignment (unique + fit)

| Page | Source strategy | Deliverable | Status |
|---|---|---|---|
| Home | Real-ESRGAN `cm-ctnt` → 16:9 | `banner-home.jpg` | done |
| Research | Real-ESRGAN `fibroblasts` (not annotated overview) | `banner-research.jpg` | done |
| Models | Real-ESRGAN `vessel-organoid` | `banner-models.jpg` | done |
| Publications | Real-ESRGAN `pericytes` | `banner-pubs.jpg` | done |
| Contact | Real-ESRGAN `smc-myh11` | `banner-contact.jpg` | done |
| 404 | Real-ESRGAN `epicardial` | `banner-404.jpg` | done |
| Join | Real-ESRGAN `tissue-culture` | `banner-join.jpg` | done |
| News | Firefly editorial illustration (no forged cells) | `banner-news.jpg` | done |
| People | Firefly cartoon/素描: Shen headshot + 5 imagined | `banner-people.jpg` | done |

Banner raster target: **2560×1440** (16:9) cover crops for mastheads.


## Sort note (featured pubs)

Already: year desc, then journal tier. Unrelated to this banner work.

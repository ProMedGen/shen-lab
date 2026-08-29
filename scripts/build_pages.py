#!/usr/bin/env python3
"""Generate static HTML pages for the Shen Lab website."""

import html
import json
import re
import subprocess
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Launch switch.
#
# While PUBLIC is False the site stays out of search indexes: every page emits
# `noindex, nofollow` and robots.txt disallows everything, which matches the
# private GitHub Pages deployment. Flipping this to True and rebuilding is the
# whole SEO half of going live -- see the launch checklist in README.md.
# ---------------------------------------------------------------------------
PUBLIC = False

# Absolute base for canonical and social-preview URLs, no trailing slash.
# Replace with the public hostname (or custom domain) when PUBLIC becomes True.
SITE_URL = "https://super-adventure-gwynznl.pages.github.io"

SITE_NAME = "Shen Lab"
SOCIAL_IMAGE = "assets/img/cm-ctnt.jpg"
SOCIAL_IMAGE_ALT = "iPSC-derived cardiomyocytes stained for cardiac troponin T"

NAV = [
    ("research.html", "Research"),
    ("models.html", "Models"),
    ("publications.html", "Publications"),
    ("news.html", "News"),
    ("people.html", "People"),
    ("join.html", "Join"),
    ("contact.html", "Contact"),
]

# Clips whose poster frame is stored under a curated name rather than
# "<stem>-poster.jpg". Kept in sync with scripts/make_posters.py.
POSTER_OVERRIDES = {
    "cm-beating.mp4": "cm-beating-poster.jpg",
    "cardiac-organoids.mp4": "cardiac-organoid-poster.jpg",
    "lab-space.mp4": "lab-space.jpg",
    "tissue-culture.mp4": "tissue-culture.jpg",
}


def nav_html(active: str) -> str:
    items = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == active else ""
        items.append(f'            <li><a href="{href}"{current}>{label}</a></li>')
    return "\n".join(items)


# ---------------------------------------------------------------------------
# Media hardening
#
# The page templates below carry plain <img> and <video> tags so they stay
# readable. Sizing, lazy-loading and poster wiring are applied here instead, in
# one pass over the generated markup, using the real dimensions of the files on
# disk. Hand-maintaining ~60 width/height pairs would drift the first time an
# asset is re-exported.
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def _image_size(rel: str) -> tuple[int, int] | None:
    path = ROOT / rel
    if not path.exists():
        return None
    if path.suffix.lower() == ".svg":
        # An SVG has no pixel size; its viewBox carries the intrinsic ratio,
        # which is all width/height attributes are for here.
        box = re.search(r'viewBox="([\d.\s-]+)"', path.read_text(encoding="utf-8"))
        if not box:
            return None
        parts = box.group(1).split()
        if len(parts) != 4:
            return None
        return round(float(parts[2])), round(float(parts[3]))
    try:
        from PIL import Image
    except ImportError:
        return None
    with Image.open(path) as im:
        return im.width, im.height


@lru_cache(maxsize=None)
def _video_size(rel: str) -> tuple[int, int] | None:
    path = ROOT / rel
    if not path.exists():
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
            check=True, capture_output=True, text=True,
        ).stdout.strip().split("x")
        return int(out[0]), int(out[1])
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError, IndexError):
        return None


def _poster_for(video_rel: str) -> str | None:
    name = Path(video_rel).name
    poster = POSTER_OVERRIDES.get(name, f"{Path(name).stem}-poster.jpg")
    rel = f"assets/img/{poster}"
    return rel if (ROOT / rel).exists() else None


def _has_attr(attrs: str, name: str) -> bool:
    """Whether an attribute is present as a whole token.

    A plain substring test is wrong here: "loop" is inside "data-loop", so
    checking for it that way silently skips adding the real loop attribute.
    """
    return re.search(rf"(?<![-\w]){re.escape(name)}(?![-\w])", attrs) is not None


def enhance_media(markup: str) -> str:
    """Add intrinsic sizing, loading hints, and video posters to a page body."""

    def fix_img(match: re.Match) -> str:
        tag, attrs = match.group(0), match.group(1)
        src = re.search(r'src="([^"]+)"', attrs)
        if not src:
            return tag
        additions = []
        if "width=" not in attrs:
            size = _image_size(src.group(1))
            if size:
                additions.append(f'width="{size[0]}" height="{size[1]}"')
        if "decoding=" not in attrs:
            additions.append('decoding="async"')
        # An above-the-fold image is marked in the template with
        # fetchpriority="high". Everything else defers, so the same file can be
        # the eager hero in one place and a lazy thumbnail in another.
        if "loading=" not in attrs and "fetchpriority=" not in attrs:
            additions.append('loading="lazy"')
        if not additions:
            return tag
        return f"<img{attrs} {' '.join(additions)}>"

    def fix_video(match: re.Match) -> str:
        attrs, source_rel = match.group(1), match.group(2)
        additions = []
        # preload="none" keeps the Models page from downloading every clip up
        # front; the poster stands in until a visitor presses play, or until
        # js/site.js starts a data-loop clip that has scrolled into view.
        if "preload=" not in attrs:
            additions.append('preload="none"')
        # Autoplaying a specimen clip requires muted+loop. `controls` stays so a
        # visitor can stop the motion, which WCAG 2.2.2 requires for anything
        # animating longer than five seconds.
        if _has_attr(attrs, "data-loop"):
            for flag in ("muted", "loop"):
                if not _has_attr(attrs, flag):
                    additions.append(flag)
        if "poster=" not in attrs:
            poster = _poster_for(source_rel)
            if poster:
                additions.append(f'poster="{poster}"')
        head = f"<video{attrs}{' ' + ' '.join(additions) if additions else ''}>"
        return head + match.group(0)[match.group(0).index(">") + 1:]

    markup = re.sub(r"<img((?:[^>]|\n)*?)>", fix_img, markup)
    markup = re.sub(
        r'<video((?:[^>]|\n)*?)>\s*<source src="([^"]+)"',
        fix_video,
        markup,
    )
    return markup


def stage_ratio(media_rel: str) -> str:
    """Inline aspect ratio for a .specimen-stage well, from the real media.

    Sizing each well to its own clip means object-fit never has to letterbox or
    crop, which is what produced the black bars around the tall EHT brightfield
    clip and the square vessel-organoid still.
    """
    size = _video_size(media_rel) if media_rel.endswith(".mp4") else _image_size(media_rel)
    if not size:
        # Falling back silently would emit different HTML than a machine with
        # the tooling installed, so the stale-output check in CI would flap.
        raise SystemExit(
            f"cannot measure {media_rel}: install ffmpeg (ffprobe) and pillow, "
            "see requirements.txt"
        )
    return f' style="--stage-ratio: {size[0]} / {size[1]}"'


def page(active: str, title: str, description: str, body: str, extra_scripts: str = "") -> str:
    robots = (
        '<meta name="robots" content="index, follow">'
        if PUBLIC
        else '<meta name="robots" content="noindex, nofollow">'
    )
    canonical = f"{SITE_URL}/{active}"
    social = f"{SITE_URL}/{SOCIAL_IMAGE}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  {robots}
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#14204a">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{social}">
  <meta property="og:image:alt" content="{SOCIAL_IMAGE_ALT}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/img/logo.png">
  <link rel="apple-touch-icon" href="assets/img/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/site.css">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="header-top">
      <a class="brand" href="index.html">
        <img src="assets/img/logo.png" alt="Shen Lab logo" width="594" height="669" fetchpriority="high">
        <span class="brand-text">
          <strong>Shen Lab</strong>
          <span>WashU Medicine</span>
        </span>
      </a>
      <p class="tagline">Human cells, CRISPR screens, new heart medicines</p>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    </div>
    <div class="nav-bar" id="site-nav">
      <nav aria-label="Primary">
        <ul>
{nav_html(active)}
        </ul>
      </nav>
    </div>
  </header>
  <main id="content">
{enhance_media(body)}
  </main>
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <a class="footer-brand" href="index.html">
        <img src="assets/img/logo.png" alt="Shen Lab, Cardiovascular Precision Medicine Lab" width="594" height="669" loading="lazy" decoding="async">
        <span class="footer-brand-text">
          <strong>Shen Lab</strong>
          <span>Cardiovascular Precision Medicine Lab</span>
        </span>
      </a>
      <div class="footer-affiliations">
        <p class="footer-copy">Division of Cardiology · Center for Cardiovascular Research · Washington University School of Medicine in St. Louis</p>
        <div class="affiliations">
          <img class="logo-washu" src="assets/img/washu-medicine.svg" alt="WashU Medicine" width="470" height="64" loading="lazy" decoding="async">
          <img class="logo-cvr" src="assets/img/cvr-center.png" alt="Center for Cardiovascular Research" width="363" height="92" loading="lazy" decoding="async">
        </div>
      </div>
    </div>
  </footer>
  <script src="js/site.js"></script>
{extra_scripts}
</body>
</html>
"""


HOME = r"""
    <section class="hero-bleed">
      <img src="assets/img/cm-ctnt.jpg" alt="iPSC-cardiomyocytes stained for cardiac troponin T" fetchpriority="high">
      <div class="hero-copy">
        <p class="kicker">WashU Medicine · Cardiology</p>
        <h1>Decoding and treating human cardiovascular disease.</h1>
        <p class="lede">The Cardiovascular Precision Medicine Lab uses human iPSCs, CRISPR screens, and organoids to find disease drivers and next-generation therapeutics.</p>
        <div class="hero-actions">
          <a class="btn btn-light" href="research.html">Learn more</a>
          <a class="btn btn-ghost" href="models.html">Watch beating cells</a>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="mission">
          <h2>Research</h2>
          <p class="mission-lead">We decode the gene programs that drive congenital and acquired cardiovascular disease — the leading cause of death worldwide.</p>
          <p>The Cardiovascular Precision Medicine Lab is led by Dr. Mengcheng Shen, PhD, with a goal to understand the genetic and cellular mechanisms that regulate the development and function of the human cardiovascular system in health and disease. Using human induced pluripotent stem cells and emerging functional-genomic, genome-editing, and organoid technologies, we are focused on decoding those programs in human cells.</p>
          <p>To translate these findings back to the clinic, the lab also develops new approaches, including novel iPSC-cardiovascular models, high-throughput CRISPR screens, and single-cell Perturb-seq coupled with virtual-cell computational models, to nominate disease drivers and deliver next-generation, precision-based therapeutics, from small molecules that prevent anti-cancer drug–induced cardiotoxicity to chemically defined cells for regenerative medicine. By building these human-relevant models entirely from human cells, in step with the NIH New Approach Methodologies (NAMs) initiative, we ultimately seek to advance the diagnosis and treatment of cardiomyopathy, congenital heart disease, and related cardiovascular disorders.</p>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">Science</p>
          <h2>Five interconnected programs</h2>
        </div>
        <div class="programs">
          <a class="program" href="research.html#differentiation">
            <img src="assets/img/cm-ctnt.jpg" alt="iPSC-cardiomyocytes">
            <div>
              <h3>Differentiation</h3>
              <p>2D and 3D cardiovascular cells, vessel organoids, and vascularized cardiac organoids from hiPSCs.</p>
            </div>
          </a>
          <a class="program" href="research.html#genomics">
            <img src="assets/img/epicardial.jpg" alt="iPSC-epicardial cells">
            <div>
              <h3>Functional genomics</h3>
              <p>CRISPR screens, VUS knock-ins, and cell-type-specific tests of non-coding variants.</p>
            </div>
          </a>
          <a class="program" href="research.html#modeling">
            <img src="assets/img/pericytes.jpg" alt="iPSC-cardiac pericytes">
            <div>
              <h3>Disease modeling</h3>
              <p>Patient iPSCs with isogenic controls for cardiomyopathy, pulmonary hypertension, and vascular disease.</p>
            </div>
          </a>
          <a class="program" href="research.html#cardio-oncology">
            <img src="assets/img/cardio-oncology.jpg" alt="Cardio-oncology illustration">
            <div>
              <h3>Precision cardio-oncology</h3>
              <p>Protect the heart during anti-cancer therapy without losing oncologic efficacy.</p>
            </div>
          </a>
          <a class="program" href="research.html#perturb-seq">
            <img src="assets/img/vessel-organoid.jpg" alt="iPSC vessel organoid">
            <div>
              <h3>Perturb-seq</h3>
              <p>Single-cell perturbation maps as training data for virtual-cell models of the heart.</p>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!--NEWS_TEASER-->

    <section>
      <div class="wrap">
        <p class="kicker">Featured publication</p>
        <article class="pub pub-feature">
          <figure class="pub-feature-media">
            <img src="assets/img/vascularized-organoids-poster.jpg" alt="Vascularized cardiac organoid from the featured Science paper">
          </figure>
          <div class="pub-feature-body">
            <p class="journal">Science · 2025</p>
            <h3>Gastruloids enable modeling of the earliest stages of human cardiac and hepatic vascularization</h3>
            <p>Abilez OJ, Yang H, Guan Y, Shen M, et al. Human pluripotent stem cell gastruloids used to study how the heart and liver first become vascularized.</p>
            <div class="chips">
              <a class="chip" href="https://doi.org/10.1126/science.adu9375">DOI</a>
              <a class="chip" href="https://pubmed.ncbi.nlm.nih.gov/40472086/">PMID</a>
              <a class="chip" href="publications.html">All publications</a>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">From the microscope</p>
          <h2>Models you can see beating</h2>
          <p>All images and movies below were generated in the lab. <a href="models.html">Open the full gallery</a>.</p>
        </div>
        <div class="mosaic">
          <a class="tile" href="models.html">
            <img src="assets/img/cm-ctnt.jpg" alt="iPSC-cardiomyocytes, cardiac troponin T">
            <span>CM · cTnT</span>
          </a>
          <a class="tile" href="models.html">
            <img src="assets/img/epicardial.jpg" alt="iPSC-epicardial cells">
            <span>Epicardial · ZO-1 / WT1</span>
          </a>
          <a class="tile" href="models.html">
            <img src="assets/img/vessel-organoid.jpg" alt="iPSC vessel organoid">
            <span>Vessel organoid</span>
          </a>
          <a class="tile" href="models.html">
            <img src="assets/img/pericytes.jpg" alt="iPSC-cardiac pericytes">
            <span>Pericytes · αSMA / PDGFRβ</span>
          </a>
          <a class="tile" href="models.html">
            <img src="assets/img/fibroblasts.jpg" alt="iPSC-cardiac fibroblasts">
            <span>Fibroblasts · TE-7</span>
          </a>
          <a class="tile" href="models.html">
            <img src="assets/img/smc-myh11.jpg" alt="iPSC-cardiac smooth muscle cells">
            <span>SMC · MYH11</span>
          </a>
        </div>
      </div>
    </section>
"""

RESEARCH = r"""
    <header class="masthead mast-research">
      <div class="wrap">
        <p class="kicker">Five programs</p>
        <h1>Our research</h1>
        <p class="lede">We combine unique access to human iPSC cardiovascular models with CRISPR screens, organoids, and computational perturbation maps.</p>
      </div>
    </header>

    <section>
      <div class="wrap two-col">
        <p>The Shen Lab integrates human induced pluripotent stem cells with high-throughput CRISPR knockout, CRISPRi, and CRISPRa screens to define the pathogenic drivers of congenital and acquired cardiovascular disease.</p>
        <p>Because the disease models are built directly from human cells, they are human-relevant and predictive, and sit inside the NIH and FDA New Approach Methodologies (NAMs) push toward the next generation of biomedical research.</p>
      </div>
    </section>

    <section>
      <div class="wrap">
        <figure class="wide-figure">
          <img src="assets/img/research-overview.jpg" alt="Lab research overview showing iPSC differentiation, CRISPR screens, disease modeling, and cardio-oncology">
          <figcaption class="caption">Lab research overview: patient iPSCs, CRISPR editing, 2D/3D cardiovascular cell types, disease modeling, and cardio-oncology screens.</figcaption>
        </figure>
      </div>
    </section>

    <section>
      <div class="wrap stack">
        <article class="topic" id="differentiation">
          <div class="topic-copy">
            <p class="kicker">Differentiation</p>
            <h2>Robust cardiovascular cells in 2D and 3D</h2>
            <p>We develop protocols to generate cardiomyocytes, endothelial cells, epicardial cells, cardiac neural crest cells, cardiac smooth muscle cells, cardiac fibroblasts, and cardiac pericytes, as well as vessel organoids and vascularized cardiac organoids. A current priority is organoids that incorporate cardiomyocytes, vascular cells, and immune cells. For regenerative medicine, we are establishing xeno-free, chemically defined protocols that perform across diverse iPSC lines.</p>
            <div class="chips">
              <a class="chip" href="https://doi.org/10.1161/CIRCULATIONAHA.122.061770">Circulation 2023 · pericytes</a>
              <a class="chip" href="https://doi.org/10.1016/j.xpro.2023.102256">STAR Protocols 2023</a>
            </div>
          </div>
          <figure class="topic-figure figure-light">
            <img src="assets/img/endothelial-protocol.jpg" alt="Xeno-free iPSC-endothelial differentiation protocol, shown in full">
            <figcaption>High-efficiency iPSC-endothelial differentiation in a xeno-free system (CD144, CD31, eNOS, vWF).</figcaption>
          </figure>
        </article>

        <article class="topic" id="genomics">
          <div class="topic-copy">
            <p class="kicker">Functional genomics</p>
            <h2>Fate decisions and variant function</h2>
            <p>We deploy genome-scale CRISPR screens to uncover master regulators of cell type–specific fate decisions. Using CRISPR genome editing, we install variants of uncertain significance into hiPSCs. We also apply deep-learning models to prioritize de novo non-coding variants predicted to drive congenital heart disease, then use CRISPR-edited iPSCs to test genotype–phenotype causality.</p>
            <div class="chips">
              <a class="chip" href="https://doi.org/10.1016/j.stem.2024.10.007">Cell Stem Cell 2024 · CRISPRi/a</a>
              <a class="chip" href="https://doi.org/10.1016/j.cell.2022.11.028">Cell 2022 · CHD variants</a>
            </div>
          </div>
        </article>

        <article class="topic" id="modeling">
          <div class="topic-copy">
            <p class="kicker">Disease modeling</p>
            <h2>Patient iPSCs with isogenic controls</h2>
            <p>Using patient-derived hiPSCs paired with CRISPR/Cas9-corrected isogenic controls, we dissect cardiomyopathy, pulmonary hypertension, and vascular disease. Druggable-genome CRISPR screens nominate disease drivers without bias and identify small molecules that mitigate or rescue diseased phenotypes.</p>
            <div class="chips">
              <a class="chip" href="https://doi.org/10.1161/CIRCULATIONAHA.124.068656">Circulation 2024 · valve cells</a>
              <a class="chip" href="https://doi.org/10.1016/j.scr.2022.102941">Stem Cell Res 2022 · TTN DCM</a>
            </div>
          </div>
          <figure class="topic-figure figure-dark">
            <img src="assets/img/pericytes.jpg" alt="iPSC-cardiac pericytes, αSMA green and PDGFRβ red, shown in full">
            <figcaption>iPSC-cardiac pericytes · αSMA (green), PDGFRβ (red).</figcaption>
          </figure>
        </article>

        <article class="topic" id="cardio-oncology">
          <div class="topic-copy">
            <p class="kicker">Precision cardio-oncology</p>
            <h2>Protect the heart without losing anti-cancer efficacy</h2>
            <p>We combine druggable-genome CRISPR screens with cancer survivors’ iPSC-derived cardiovascular cells to identify therapeutic targets that reduce anti-cancer drug-induced cardiovascular toxicity without compromising oncologic efficacy.</p>
            <div class="chips">
              <a class="chip" href="https://doi.org/10.1002/advs.202510543">Adv Sci 2026 · cardiotoxicity</a>
              <a class="chip" href="https://doi.org/10.1161/CIRCULATIONAHA.124.071217">Circulation 2025 · CD47</a>
            </div>
          </div>
          <figure class="topic-figure figure-dark">
            <img src="assets/img/crispr-pipeline.jpg" alt="CRISPR screen pipeline for precision cardio-oncology, shown in full">
            <figcaption>CRISPR screen pipeline in precision cardio-oncology.</figcaption>
          </figure>
        </article>

        <article class="topic" id="perturb-seq">
          <div class="topic-copy">
            <p class="kicker">Perturb-seq</p>
            <h2>Training data for virtual-cell models</h2>
            <p>We are generating physiologically relevant single-cell Perturb-seq datasets in iPSC-derived cardiovascular cells to train virtual-cell foundation models, advancing scalable in silico approaches to cardiovascular research.</p>
            <div class="chips">
              <a class="chip" href="https://doi.org/10.1126/science.adu9375">Science 2025 · gastruloids</a>
            </div>
          </div>
          <figure class="topic-figure figure-dark">
            <img src="assets/img/vessel-organoid.jpg" alt="iPSC vessel organoid with stain legend, shown in full">
            <figcaption>iPSC-vessel organoid · DAPI | VE-cadherin | CD31 | PDGFRβ.</figcaption>
          </figure>
        </article>
      </div>
    </section>

    <section>
      <div class="wrap nams">
        <div>
          <p class="kicker">NIH / FDA</p>
          <h2>Alignment with New Approach Methodologies</h2>
          <p>NAMs are in vitro, in chemico, and in silico approaches designed to model human biology more accurately than traditional animal models. In April 2025, NIH announced a strategic shift toward human-based research technologies, and FDA released a parallel roadmap to reduce animal testing in preclinical safety studies.</p>
        </div>
        <ul>
          <li><strong>Human in vitro models.</strong> hiPSC cardiovascular cell types, vessel organoids, and vascularized cardiac organoids.</li>
          <li><strong>Mechanism and safety.</strong> Patient/isogenic models, VUS knock-ins, and cardio-oncology screens.</li>
          <li><strong>In silico modeling.</strong> Perturb-seq datasets and virtual-cell foundation models.</li>
        </ul>
      </div>
    </section>
"""

MODELS = rf"""
    <header class="masthead mast-models">
      <div class="wrap">
        <p class="kicker">Cell atlas</p>
        <h1>A cardiovascular cell atlas grown from hiPSCs</h1>
        <p class="lede">Live beating cultures, stained lineages, vessel and cardiac organoids, and the rooms where the work happens.</p>
      </div>
    </header>

    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">Live</p>
          <h2>Beating cells and tissues</h2>
          <p>Beating monolayers and engineered heart tissues recorded in culture. Clips loop silently; use the controls to pause or scrub.</p>
        </div>
        <div class="clip-row">
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/cm-beating.mp4")}>
              <video controls playsinline poster="assets/img/cm-beating-poster.jpg" data-loop>
                <source src="assets/video/cm-beating.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>Beating cardiomyocytes</strong>
              <span>Brightfield live culture</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/eht-myl7.mp4")}>
              <video controls playsinline data-loop>
                <source src="assets/video/eht-myl7.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>Engineered heart tissue</strong>
              <span>MYL7-eGFP</span>
            </figcaption>
          </figure>
        </div>
        <div class="clip-row clip-row-tall">
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/cm-myl7.mp4")}>
              <video controls playsinline data-loop>
                <source src="assets/video/cm-myl7.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>MYL7 reporter cardiomyocytes</strong>
              <span>Live fluorescence, green beating reporter</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/eht-brightfield.mp4")}>
              <video controls playsinline data-loop>
                <source src="assets/video/eht-brightfield.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>Engineered heart tissue</strong>
              <span>Brightfield</span>
            </figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">Stains</p>
          <h2>Lineages</h2>
          <p>The main iPSC-derived cardiovascular cell types used in the lab.</p>
        </div>
        <div class="atlas-grid">
          <figure class="specimen">
            <div class="specimen-stage">
            <img src="assets/img/cm-ctnt.jpg" alt="iPSC-cardiomyocytes, cardiac troponin T in red">
            </div>
            <figcaption>
              <strong>Cardiomyocytes</strong>
              <span>Cardiac troponin T</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage">
            <img src="assets/img/epicardial.jpg" alt="iPSC-epicardial cells, ZO-1 red and WT1 cyan">
            </div>
            <figcaption>
              <strong>Epicardial cells</strong>
              <span>ZO-1 and WT1</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage">
            <img src="assets/img/pericytes.jpg" alt="iPSC-cardiac pericytes">
            </div>
            <figcaption>
              <strong>Cardiac pericytes</strong>
              <span>αSMA and PDGFRβ</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage">
            <img src="assets/img/fibroblasts.jpg" alt="iPSC-cardiac fibroblasts">
            </div>
            <figcaption>
              <strong>Cardiac fibroblasts</strong>
              <span>TE-7</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage">
            <img src="assets/img/smc-myh11.jpg" alt="iPSC-cardiac smooth muscle cells">
            </div>
            <figcaption>
              <strong>Smooth muscle cells</strong>
              <span>MYH11</span>
            </figcaption>
          </figure>
        </div>
        <figure class="specimen specimen-wide">
          <div class="specimen-stage"{stage_ratio("assets/img/endothelial-protocol.jpg")}>
          <img src="assets/img/endothelial-protocol.jpg" alt="Xeno-free iPSC-endothelial differentiation: flow cytometry for CD144 and CD31, and immunostaining for eNOS and vWF">
          </div>
          <figcaption>
            <strong>Endothelial cells</strong>
            <span>High-efficiency xeno-free differentiation, characterised by CD144, CD31, eNOS, and vWF.</span>
          </figcaption>
        </figure>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">3D</p>
          <h2>Organoids</h2>
          <p>Cardiac organoids, vascularized cardiac organoids, and vessel organoids.</p>
        </div>
        <div class="clip-row">
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/cardiac-organoids.mp4")}>
              <video controls playsinline poster="assets/img/cardiac-organoid-poster.jpg" data-loop>
                <source src="assets/video/cardiac-organoids.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>Cardiac organoids</strong>
              <span>Beating 3D culture</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/vascularized-organoids.mp4")}>
              <video controls playsinline data-loop>
                <source src="assets/video/vascularized-organoids.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>Vascularized cardiac organoids</strong>
              <span>Live culture</span>
            </figcaption>
          </figure>
        </div>
        <div class="clip-row">
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/img/vessel-organoid.jpg")}>
            <img src="assets/img/vessel-organoid.jpg" alt="iPSC vessel organoid stained for DAPI, VE-cadherin, CD31, PDGFRβ">
            </div>
            <figcaption>
              <strong>Vessel organoid</strong>
              <span>DAPI, VE-cadherin, CD31, PDGFRβ</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/vessel-organoids.mp4")}>
              <video controls playsinline data-loop>
                <source src="assets/video/vessel-organoids.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>Vessel organoids</strong>
              <span>CD31, PDGFRβ, collagen IV</span>
            </figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">Rooms</p>
          <h2>Lab spaces</h2>
          <p>Where the cultures are grown.</p>
        </div>
        <div class="clip-row">
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/lab-space.mp4")}>
              <video controls playsinline poster="assets/img/lab-space.jpg">
                <source src="assets/video/lab-space.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>Laboratory</strong>
              <span>Open bench space</span>
            </figcaption>
          </figure>
          <figure class="specimen">
            <div class="specimen-stage"{stage_ratio("assets/video/tissue-culture.mp4")}>
              <video controls playsinline poster="assets/img/tissue-culture.jpg">
                <source src="assets/video/tissue-culture.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>
              <strong>Tissue culture</strong>
              <span>Sterile culture room</span>
            </figcaption>
          </figure>
        </div>
      </div>
    </section>
"""

PEOPLE = r"""
    <header class="masthead mast-people">
      <div class="wrap">
        <p class="kicker">The lab</p>
        <h1>Our team</h1>
        <p class="lede">The lab is a growing group at the intersection of stem-cell models, CRISPR screens, and cardiovascular disease. We value careful experiments, collaboration, and questions that only human cells can answer.</p>
      </div>
    </header>

    <section>
      <div class="wrap">
        <h2>Principal investigator</h2>
        <article class="pi">
          <img src="assets/img/headshot.jpg" alt="Portrait of Mengcheng Shen, PhD">
          <div>
            <h3>Mengcheng Shen, PhD</h3>
            <p class="pi-title">Assistant Professor of Medicine and of Developmental Biology</p>
            <p>Washington University School of Medicine in St. Louis. The lab uses high-throughput stem-cell and CRISPR-screen platforms to study genetic-variant and drug-induced cardiovascular pathologies, advancing precision cardiovascular medicine.</p>
            <ul class="meta">
              <li>Division of Cardiology</li>
              <li>Center for Cardiovascular Research</li>
              <li>Center of Regenerative Medicine</li>
              <li>Siteman Cancer Center</li>
              <li>ICTS</li>
            </ul>
            <div class="chips">
              <a class="chip" href="https://cardiology.wustl.edu/people/mengcheng-shen-phd/">Faculty page</a>
              <a class="chip" href="https://profiles.wustl.edu/en/persons/mengcheng-shen">Research profile</a>
              <a class="chip" href="https://orcid.org/0000-0001-7037-6159">ORCID</a>
              <a class="chip" href="https://med.stanford.edu/wulab/former-trainees.html">Stanford Wu lab</a>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section class="cv-band">
      <div class="wrap cv-honors-grid">
        <div>
          <p class="kicker">Curriculum</p>
          <h2>Appointments, education, and training</h2>
          <ol class="cv-list">
            <li class="cv-current">
              <span class="cv-years">2025–present</span>
              <div>
                <strong>Assistant Professor of Medicine</strong>
                <p>Washington University School of Medicine, since May 2025. Division of Cardiology; also Assistant Professor of Developmental Biology.</p>
              </div>
            </li>
            <li>
              <span class="cv-years">2023–2025</span>
              <div>
                <strong>Instructor</strong>
                <p>Stanford Cardiovascular Institute. Joseph C. Wu laboratory.</p>
              </div>
            </li>
            <li>
              <span class="cv-years">2018–2023</span>
              <div>
                <strong>Postdoctoral fellow</strong>
                <p>Stanford Cardiovascular Institute. Mentor: Joseph C. Wu, MD, PhD.</p>
              </div>
            </li>
            <li>
              <span class="cv-years">2018</span>
              <div>
                <strong>PhD, Physiology</strong>
                <p>University of Alberta, Edmonton, Canada. Mentor: Zamaneh Kassiri, PhD.</p>
              </div>
            </li>
            <li>
              <span class="cv-years">2012</span>
              <div>
                <strong>MSc, Nutrition</strong>
                <p>Nanjing Agricultural University, Nanjing, China.</p>
              </div>
            </li>
            <li>
              <span class="cv-years">2009</span>
              <div>
                <strong>BSc, Animal Science</strong>
                <p>Nanjing Agricultural University, Nanjing, China.</p>
              </div>
            </li>
          </ol>
        </div>
        <div>
          <p class="kicker">Recognition</p>
          <h2>Honors and awards</h2>
          <article class="honor-feature">
            <p class="kicker">NIH career award</p>
            <h3>NHLBI K99/R00 Pathway to Independence Award</h3>
            <p>2023 · National Heart, Lung, and Blood Institute</p>
          </article>
          <ul class="honors-list">
            <li>
              <span class="honor-year">2024</span>
              <span class="honor-name">Best Poster Award, Stanford Bio-X Interdisciplinary Initiatives Seed Grants Program</span>
            </li>
            <li>
              <span class="honor-year">2022</span>
              <span class="honor-name">Best Poster Award, Stanford–Weill Cornell Cardiovascular Research Symposium</span>
            </li>
            <li>
              <span class="honor-year">2018</span>
              <span class="honor-name">Peter Pang Best Ph.D. Thesis Award, University of Alberta</span>
            </li>
            <li>
              <span class="honor-year">2018</span>
              <span class="honor-name">Med Star Publication Award for Graduate Student</span>
            </li>
            <li>
              <span class="honor-year">2018</span>
              <span class="honor-name">Dr. Francis X. Witkowski Publication Award</span>
            </li>
            <li>
              <span class="honor-year">2018</span>
              <span class="honor-name">Best Basic Science Podium Research Presentation Award</span>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <h2>Lab members</h2>
        <p class="lede">Current members of the Cardiovascular Precision Medicine Lab. Open roles below remain actively recruiting.</p>
        <div class="team-grid">
          <a class="person-card person-card-named" href="mailto:rshang@wustl.edu">
            <div class="person-mark" aria-hidden="true">SR</div>
            <div class="person-body">
              <p class="person-role">Postdoc</p>
              <h3>Renjie Shang</h3>
              <p>Postdoctoral Research Associate · DOM Cardiology</p>
            </div>
          </a>
          <a class="person-card person-card-named" href="mailto:zhanyu@wustl.edu">
            <div class="person-mark" aria-hidden="true">IZ</div>
            <div class="person-body">
              <p class="person-role">Visiting researcher</p>
              <h3>Ivy Zhong</h3>
              <p>Visiting Researcher · DOM Cardiology</p>
            </div>
          </a>
          <a class="person-card person-card-open" href="join.html">
            <div class="person-mark" aria-hidden="true">PD</div>
            <div class="person-body">
              <p class="person-role">Position open</p>
              <h3>Postdoctoral fellow</h3>
              <p>iPSC models, CRISPR screens, cardio-oncology</p>
            </div>
          </a>
          <a class="person-card person-card-open" href="join.html">
            <div class="person-mark" aria-hidden="true">GS</div>
            <div class="person-body">
              <p class="person-role">Position open</p>
              <h3>Graduate student</h3>
              <p>PhD and MSTP students at WashU</p>
            </div>
          </a>
          <a class="person-card person-card-open" href="join.html">
            <div class="person-mark" aria-hidden="true">RS</div>
            <div class="person-body">
              <p class="person-role">Position open</p>
              <h3>Research staff</h3>
              <p>Technician or staff scientist</p>
            </div>
          </a>
          <a class="person-card person-card-open" href="join.html">
            <div class="person-mark" aria-hidden="true">UG</div>
            <div class="person-body">
              <p class="person-role">Position open</p>
              <h3>Undergraduate / rotation</h3>
              <p>Short-term research in the lab</p>
            </div>
          </a>
        </div>
        <p class="team-note">If you want to fill one of these seats, see <a href="join.html">Join</a>.</p>
      </div>
    </section>
"""

JOIN = r"""
    <header class="masthead mast-join">
      <div class="wrap">
        <p class="kicker">Open roles</p>
        <h1>Join our team</h1>
        <p class="lede">We are looking for people who want to work at the intersection of stem-cell models, functional genomics, and cardiovascular disease.</p>
      </div>
    </header>

    <section>
      <div class="wrap prose">
        <p>The lab is recruiting postdoctoral fellows, graduate students, and other trainees. We are looking for creative, self-motivated, and collaborative people who want to advance their training in human cardiovascular biology. Candidates with experience in genomics, bioinformatics, molecular biology, iPSC culture, or CRISPR screening are encouraged.</p>
        <p>Dr. Shen is listed as willing to mentor PhD and MSTP students at Washington University.</p>
        <p>To inquire, start from the WashU faculty page with a short note and a CV.</p>
        <p><a class="btn btn-primary" href="https://cardiology.wustl.edu/people/mengcheng-shen-phd/">Faculty page</a> <a class="btn btn-ghost" href="contact.html">Contact</a></p>
      </div>
    </section>
"""

CONTACT = r"""
    <header class="masthead mast-contact">
      <div class="wrap">
        <p class="kicker">St. Louis</p>
        <h1>Get in touch</h1>
        <p class="lede">Write to Dr. Shen, or visit the lab on the WashU Medical Center campus in St. Louis.</p>
      </div>
    </header>

    <section>
      <div class="wrap contact-grid">
        <div>
          <h2>Principal investigator</h2>
          <p class="contact-name">Mengcheng Shen, PhD</p>
          <p>Assistant Professor of Medicine and of Developmental Biology<br>Division of Cardiology, WashU Medicine</p>
          <dl class="contact-dl">
            <div>
              <dt>Email</dt>
              <dd><a href="mailto:shen.m@wustl.edu">shen.m@wustl.edu</a></dd>
            </div>
            <div>
              <dt>Faculty</dt>
              <dd><a href="https://cardiology.wustl.edu/people/mengcheng-shen-phd/">Cardiology faculty page</a></dd>
            </div>
            <div>
              <dt>Profile</dt>
              <dd><a href="https://profiles.wustl.edu/en/persons/mengcheng-shen">WashU Research Profiles</a></dd>
            </div>
            <div>
              <dt>ORCID</dt>
              <dd><a href="https://orcid.org/0000-0001-7037-6159">0000-0001-7037-6159</a></dd>
            </div>
          </dl>
          <p><a class="btn btn-primary" href="mailto:shen.m@wustl.edu">Email Dr. Shen</a> <a class="btn btn-ghost" href="join.html">Join the lab</a></p>
        </div>
        <div>
          <h2>Visit</h2>
          <p>Cardiovascular Division administrative offices, WashU Medical Center campus:</p>
          <p class="contact-address">
            4940 Parkview Place<br>
            St. Louis, MO 63110
          </p>
          <p><a href="https://maps.google.com/?q=4940+Parkview+Place,+St.+Louis,+MO+63110">Open in Google Maps</a></p>
          <div class="affiliations">
            <img class="logo-lab" src="assets/img/logo.png" alt="Shen Lab logo">
            <img class="logo-washu" src="assets/img/washu-medicine.svg" alt="WashU Medicine">
            <img class="logo-cvr" src="assets/img/cvr-center.png" alt="Center for Cardiovascular Research">
          </div>
        </div>
      </div>
    </section>

    <section class="map-band">
      <div class="wrap">
        <div class="map-embed map-embed-large">
          <iframe title="Map of WashU Medical Center, 4940 Parkview Place, St. Louis"
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3116.4!2d-90.2638319!3d38.6382822!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x87d8b4c6%3A0x0!2s4940%20Parkview%20Place%2C%20St.%20Louis%2C%20MO%2063110!5e0!3m2!1sen!2sus!4v1710000000000!5m2!1sen!2sus"
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
            allowfullscreen></iframe>
        </div>
      </div>
    </section>
"""

def _authors_html(names: list[str]) -> str:
    bits = []
    for name in names:
        if name == "Shen M":
            bits.append(f"<strong>{html.escape(name)}</strong>")
        else:
            bits.append(html.escape(name))
    return ", ".join(bits)


def _venue(paper: dict) -> str:
    journal = html.escape(paper["journal"])
    year = paper["year"]
    loc = paper.get("volume") or ""
    if loc and paper.get("issue"):
        loc += f"({paper['issue']})"
    if loc and paper.get("pages"):
        loc += f":{html.escape(paper['pages'])}"
    elif paper.get("pages"):
        loc = html.escape(paper["pages"])
    if loc:
        return f"{journal}. {year}; {loc}."
    return f"{journal}. {year}."


def load_news() -> list:
    items = json.loads((ROOT / "data" / "news.json").read_text(encoding="utf-8"))
    return sorted(items, key=lambda item: item["date"], reverse=True)


def _news_card(item: dict, level: int) -> str:
    """Render one news item. `level` is the heading level for its title.

    On news.html the items sit directly under the page h1, so they are h2. In
    the home-page teaser they sit under the section's own h2, so they are h3.
    Getting this wrong is what tripped the axe heading-order check.
    """
    title = html.escape(item["title"])
    summary = html.escape(item["summary"])
    source = html.escape(item["source"])
    kind = html.escape(item["kind"])
    date = html.escape(item["display_date"])
    url = html.escape(item["url"], quote=True)
    return f"""
        <article class="news-item">
          <div class="news-meta">
            <p class="news-date">{date}</p>
            <p class="news-kind">{kind}</p>
          </div>
          <div>
            <h{level} class="news-title"><a href="{url}">{title}</a></h{level}>
            <p>{summary}</p>
            <p class="news-source">{source}</p>
          </div>
        </article>"""


def build_news_teaser() -> str:
    items = load_news()[:3]
    cards = "".join(_news_card(item, 3) for item in items)
    return f"""
    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">News</p>
          <h2>Lab news and media coverage</h2>
          <p>Institutional announcements, awards, and press on Dr. Shen's work. <a href="news.html">All news</a>.</p>
        </div>
        <div class="news-list">{cards}
        </div>
      </div>
    </section>
"""


def build_news() -> str:
    items = load_news()
    cards = "".join(_news_card(item, 2) for item in items)
    return f"""
    <header class="masthead mast-news">
      <div class="wrap">
        <p class="kicker">Updates</p>
        <h1>Lab news and media</h1>
        <p class="lede">Documented awards, institutional announcements, and press coverage of Dr. Shen's work. Named team-member news will be added as people join.</p>
      </div>
    </header>

    <section>
      <div class="wrap">
        <div class="news-list">{cards}
        </div>
        <p class="team-note">Send a link if we missed coverage of the lab or of a team member. Papers themselves stay on <a href="publications.html">Publications</a>.</p>
      </div>
    </section>
"""


def build_publications() -> str:
    papers = json.loads((ROOT / "data" / "publications.json").read_text(encoding="utf-8"))
    by_year: dict[int, list] = defaultdict(list)
    for paper in papers:
        by_year[paper["year"]].append(paper)
    years = sorted(by_year, reverse=True)
    jumps = "".join(f'<a href="#y{year}">{year}</a>' for year in years)
    blocks = []
    for year in years:
        rows = []
        for paper in by_year[year]:
            doi = paper.get("doi") or ""
            pmid = paper["pmid"]
            title = html.escape(paper["title"])
            title_html = (
                f'<a href="https://doi.org/{html.escape(doi)}">{title}</a>' if doi else title
            )
            chips = []
            if doi:
                chips.append(f'<a class="chip" href="https://doi.org/{html.escape(doi)}">DOI</a>')
            chips.append(f'<a class="chip" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/">PubMed</a>')
            metrics = ""
            if doi:
                metrics = f"""
          <div class="pub-metrics">
            <div class="altmetric-embed" data-badge-type="donut" data-doi="{html.escape(doi)}" data-hide-no-mentions="true" data-link-target="_blank"></div>
            <span class="__dimensions_badge_embed__" data-doi="{html.escape(doi)}" data-hide-zero-citations="true" data-style="small_circle" data-legend="hover-right"></span>
          </div>"""
            rows.append(
                f"""
        <article class="pub-row">
          <div class="pub-main">
            <h3>{title_html}</h3>
            <p class="pub-authors">{_authors_html(paper["authors"])}</p>
            <p class="pub-venue">{_venue(paper)}</p>
            <div class="chips">{"".join(chips)}</div>
          </div>{metrics}
        </article>"""
            )
        blocks.append(
            f"""
      <h2 class="year" id="y{year}">{year}</h2>
      <div class="pub-list">{"".join(rows)}
      </div>"""
        )
    return f"""
    <header class="masthead mast-pubs">
      <div class="wrap">
        <p class="kicker">2014–2026</p>
        <h1>Publications</h1>
      </div>
    </header>

    <section>
      <div class="wrap">
        <nav class="year-nav" aria-label="Years">{jumps}</nav>
        {"".join(blocks)}
        <p>Also listed on the <a href="https://profiles.wustl.edu/en/persons/mengcheng-shen/publications/">WashU research profile</a>.</p>
      </div>
    </section>
"""



NOT_FOUND = """
    <header class="masthead mast-404">
      <div class="wrap">
        <p class="kicker">404</p>
        <h1>That page is not on this site.</h1>
        <p class="lede">The link may be out of date, or the page may have moved. Everything on the site is reachable from the menu above.</p>
      </div>
    </header>

    <section>
      <div class="wrap prose">
        <h2>Try one of these</h2>
        <ul class="refs">
          <li><a href="index.html">Home</a> — what the lab works on, in brief.</li>
          <li><a href="research.html">Research</a> — the five programs, with figures and papers.</li>
          <li><a href="models.html">Models</a> — beating cells, organoids, and stained lineages.</li>
          <li><a href="publications.html">Publications</a> — every paper, grouped by year.</li>
          <li><a href="join.html">Join</a> — open positions and how to apply.</li>
          <li><a href="contact.html">Contact</a> — email, address, and map.</li>
        </ul>
      </div>
    </section>
"""


def build_sitemap(page_names: list[str]) -> str:
    """Emit sitemap.xml. Harmless while the site is private; required at launch."""
    urls = "\n".join(
        f"  <url><loc>{SITE_URL}/{name}</loc></url>" for name in page_names
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )


def build_robots() -> str:
    if PUBLIC:
        return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    return "User-agent: *\nDisallow: /\n"


def main() -> None:
    pages = {
        "index.html": (
            "index.html",
            "Shen Lab · Cardiovascular Precision Medicine",
            "Cardiovascular Precision Medicine Lab at WashU Medicine, led by Mengcheng Shen, PhD.",
            HOME.replace("    <!--NEWS_TEASER-->\n", build_news_teaser()),
        ),
        "research.html": (
            "research.html",
            "Research · Shen Lab",
            "Research programs of the Shen Lab: differentiation, CRISPR screens, disease modeling, cardio-oncology, and Perturb-seq.",
            RESEARCH,
        ),
        "models.html": (
            "models.html",
            "Models · Shen Lab",
            "iPSC-derived cardiovascular cell types, organoids, engineered heart tissues, and lab spaces.",
            MODELS,
        ),
        "people.html": (
            "people.html",
            "People · Shen Lab",
            "Mengcheng Shen, PhD, principal investigator of the Cardiovascular Precision Medicine Lab.",
            PEOPLE,
        ),
        "join.html": (
            "join.html",
            "Join · Shen Lab",
            "Join the Cardiovascular Precision Medicine Lab at Washington University School of Medicine.",
            JOIN,
        ),
        "contact.html": (
            "contact.html",
            "Contact · Shen Lab",
            "Contact the Cardiovascular Precision Medicine Lab at WashU Medicine.",
            CONTACT,
        ),
        "publications.html": (
            "publications.html",
            "Publications · Shen Lab",
            "Publications from the Shen Lab and collaborators.",
            build_publications(),
        ),
        "news.html": (
            "news.html",
            "News · Shen Lab",
            "Lab news, awards, and media coverage of Mengcheng Shen and the Shen Lab.",
            build_news(),
        ),
    }
    extra = {
        "publications.html": """
  <script src="https://d1bxh8uas1mnw7.cloudfront.net/assets/embed.js"></script>
  <script async src="https://badge.dimensions.ai/badge.js" charset="utf-8"></script>
"""
    }
    for name, (active, title, desc, body) in pages.items():
        (ROOT / name).write_text(
            page(active, title, desc, body, extra.get(name, "")),
            encoding="utf-8",
        )
        print("wrote", name)

    # 404 goes through the same shell so a stranded visitor still gets the nav.
    # `active` is a page that is not in NAV, so nothing is marked current.
    (ROOT / "404.html").write_text(
        page("404.html", "Page not found · Shen Lab",
             "That page is not on the Shen Lab site.", NOT_FOUND),
        encoding="utf-8",
    )
    print("wrote 404.html")

    (ROOT / "sitemap.xml").write_text(build_sitemap(list(pages)), encoding="utf-8")
    print("wrote sitemap.xml")
    (ROOT / "robots.txt").write_text(build_robots(), encoding="utf-8")
    print(f"wrote robots.txt (PUBLIC={PUBLIC})")


if __name__ == "__main__":
    main()

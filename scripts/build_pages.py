#!/usr/bin/env python3
"""Generate static HTML pages for the Shen Lab website."""

import html
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Volumes/CrucialX10A/Apps/Website/Shen_Lab")

NAV = [
    ("research.html", "Research"),
    ("models.html", "Models"),
    ("publications.html", "Publications"),
    ("news.html", "News"),
    ("people.html", "People"),
    ("join.html", "Join"),
    ("contact.html", "Contact"),
]


def nav_html(active: str) -> str:
    items = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == active else ""
        items.append(f'            <li><a href="{href}"{current}>{label}</a></li>')
    return "\n".join(items)


def page(active: str, title: str, description: str, body: str, extra_scripts: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="noindex, nofollow">
  <link rel="icon" href="assets/img/logo.png">
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
        <img src="assets/img/logo.png" alt="Shen Lab logo">
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
{body}
  </main>
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <a class="footer-brand" href="index.html">
        <img src="assets/img/logo.png" alt="Shen Lab, Cardiovascular Precision Medicine Lab">
        <span class="footer-brand-text">
          <strong>Shen Lab</strong>
          <span>Cardiovascular Precision Medicine Lab</span>
        </span>
      </a>
      <div class="footer-affiliations">
        <p class="footer-copy">Division of Cardiology · Center for Cardiovascular Research · Washington University School of Medicine in St. Louis</p>
        <div class="affiliations">
          <img class="logo-washu" src="assets/img/washu-medicine.svg" alt="WashU Medicine">
          <img class="logo-cvr" src="assets/img/cvr-center.png" alt="Center for Cardiovascular Research">
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
      <img src="assets/img/cm-ctnt.jpg" alt="iPSC-cardiomyocytes stained for cardiac troponin T">
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
          <p>The Cardiovascular Precision Medicine Lab is led by Dr. Mengcheng Shen, PhD, with a goal to understand the genetic and cellular mechanisms that regulate the development and function of the human cardiovascular system in health and disease. Using human induced pluripotent stem cells and emerging functional-genomic, genome-editing, and organoid technologies, we are focused on decoding the gene programs that drive congenital and acquired cardiovascular disease, the leading cause of death worldwide.</p>
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
        <article class="pub">
          <p class="journal">Science · 2025</p>
          <h3>Gastruloids enable modeling of the earliest stages of human cardiac and hepatic vascularization</h3>
          <p>Abilez OJ, Yang H, Guan Y, Shen M, et al. Human pluripotent stem cell gastruloids used to study how the heart and liver first become vascularized.</p>
          <div class="chips">
            <a class="chip" href="https://doi.org/10.1126/science.adu9375">DOI</a>
            <a class="chip" href="https://pubmed.ncbi.nlm.nih.gov/40472086/">PMID</a>
            <a class="chip" href="publications.html">All publications</a>
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
        <p class="kicker">Research</p>
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

MODELS = r"""
    <header class="masthead mast-models">
      <div class="wrap">
        <p class="kicker">Models</p>
        <h1>A cardiovascular cell atlas grown from hiPSCs</h1>
        <p class="lede">2D lineages, engineered heart tissues, vessel organoids, and vascularized cardiac organoids, plus the rooms where the work happens.</p>
      </div>
    </header>

    <section>
      <div class="wrap">
        <h2>Beating cells and tissues</h2>
        <div class="gallery">
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline poster="assets/img/cm-beating-poster.jpg">
                <source src="assets/video/cm-beating.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>iPSC-cardiomyocytes, brightfield beating culture.</figcaption>
          </figure>
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline>
                <source src="assets/video/eht-myl7.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>iPSC-engineered heart tissues, MYL7-eGFP.</figcaption>
          </figure>
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline>
                <source src="assets/video/cm-myl7.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>iPSC-cardiomyocytes, MYL7 (green) beating reporter.</figcaption>
          </figure>
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline>
                <source src="assets/video/eht-brightfield.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>iPSC-engineered heart tissues, brightfield.</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <h2>Lineages</h2>
        <div class="gallery">
          <figure class="figure-card">
            <img src="assets/img/cm-ctnt.jpg" alt="iPSC-cardiomyocytes, cardiac troponin T in red">
            <figcaption>iPSC-cardiomyocytes · cardiac troponin T (red).</figcaption>
          </figure>
          <figure class="figure-card">
            <img src="assets/img/epicardial.jpg" alt="iPSC-epicardial cells, ZO-1 red and WT1 cyan">
            <figcaption>iPSC-epicardial cells · ZO-1 (red), WT1 (cyan).</figcaption>
          </figure>
          <figure class="figure-card">
            <img src="assets/img/pericytes.jpg" alt="iPSC-cardiac pericytes">
            <figcaption>iPSC-cardiac pericytes · αSMA (green), PDGFRβ (red).</figcaption>
          </figure>
          <figure class="figure-card">
            <img src="assets/img/fibroblasts.jpg" alt="iPSC-cardiac fibroblasts">
            <figcaption>iPSC-cardiac fibroblasts · TE-7 (red).</figcaption>
          </figure>
          <figure class="figure-card">
            <img src="assets/img/smc-myh11.jpg" alt="iPSC-cardiac smooth muscle cells">
            <figcaption>iPSC-cardiac smooth muscle cells · MYH11 (red).</figcaption>
          </figure>
          <figure class="figure-card">
            <img src="assets/img/endothelial-protocol.jpg" alt="Endothelial differentiation figure">
            <figcaption>Xeno-free endothelial differentiation with CD144 / CD31 / eNOS / vWF.</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <h2>Organoids</h2>
        <div class="gallery">
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline poster="assets/img/cardiac-organoid-poster.jpg">
                <source src="assets/video/cardiac-organoids.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>iPSC-cardiac organoids.</figcaption>
          </figure>
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline>
                <source src="assets/video/vascularized-organoids.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>iPSC-vascularized cardiac organoids.</figcaption>
          </figure>
          <figure class="figure-card">
            <img src="assets/img/vessel-organoid.jpg" alt="iPSC vessel organoid stained for DAPI, VE-cadherin, CD31, PDGFRβ">
            <figcaption>iPSC-vessel organoid · DAPI | VE-cadherin | CD31 | PDGFRβ.</figcaption>
          </figure>
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline>
                <source src="assets/video/vessel-organoids.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>iPSC-vessel organoids · CD31 (magenta), PDGFRβ (yellow), collagen IV (cyan).</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <h2>Lab spaces</h2>
        <div class="gallery">
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline poster="assets/img/lab-space.jpg">
                <source src="assets/video/lab-space.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>Laboratory space.</figcaption>
          </figure>
          <figure class="figure-card">
            <div class="media">
              <video controls playsinline poster="assets/img/tissue-culture.jpg">
                <source src="assets/video/tissue-culture.mp4" type="video/mp4">
              </video>
            </div>
            <figcaption>Tissue culture room.</figcaption>
          </figure>
        </div>
      </div>
    </section>
"""

PEOPLE = r"""
    <header class="masthead mast-people">
      <div class="wrap">
        <p class="kicker">People</p>
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
          <h2>Education and training</h2>
          <ol class="cv-list">
            <li class="cv-stanford">
              <span class="cv-years">2023–2025</span>
              <div>
                <strong>Instructor</strong>
                <p>Stanford Cardiovascular Institute. Joseph C. Wu laboratory.</p>
              </div>
            </li>
            <li class="cv-stanford">
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
        <p class="lede">Named profiles will appear here as people join. Open seats below are placeholders for the roles we are recruiting.</p>
        <div class="team-grid">
          <article class="person-card person-card-filled">
            <img src="assets/img/headshot.jpg" alt="Portrait of Mengcheng Shen, PhD">
            <div class="person-body">
              <p class="person-role">Principal investigator</p>
              <h3>Mengcheng Shen, PhD</h3>
              <p>Assistant Professor of Medicine</p>
            </div>
          </article>
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
        <p class="kicker">Join</p>
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
        <p class="kicker">Contact</p>
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


def _news_card(item: dict) -> str:
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
            <h3><a href="{url}">{title}</a></h3>
            <p>{summary}</p>
            <p class="news-source">{source}</p>
          </div>
        </article>"""


def build_news_teaser() -> str:
    items = load_news()[:3]
    cards = "".join(_news_card(item) for item in items)
    return f"""
    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">News</p>
          <h2>Lab news and coverage</h2>
          <p>Institutional announcements, awards, and press on Dr. Shen's work. <a href="news.html">All news</a>.</p>
        </div>
        <div class="news-list">{cards}
        </div>
      </div>
    </section>
"""


def build_news() -> str:
    items = load_news()
    cards = "".join(_news_card(item) for item in items)
    return f"""
    <header class="masthead mast-news">
      <div class="wrap">
        <p class="kicker">News</p>
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
        <p class="kicker">Publications</p>
        <h1>Publications</h1>
        <p class="lede">{len(papers)} papers, grouped by year. Lab member <strong>Shen M</strong> is in bold. Altmetric and Dimensions badges load when those services have a record for the DOI.</p>
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


if __name__ == "__main__":
    main()

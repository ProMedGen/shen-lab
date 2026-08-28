#!/usr/bin/env python3
"""Generate static HTML pages for the Shen Lab website."""

from pathlib import Path

ROOT = Path("/Volumes/CrucialX10A/Apps/Website/Shen_Lab")

NAV = [
    ("index.html", "Home"),
    ("research.html", "Research"),
    ("models.html", "Models"),
    ("people.html", "People"),
    ("join.html", "Join"),
]


def nav_html(active: str) -> str:
    items = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == active else ""
        items.append(f'          <li><a href="{href}"{current}>{label}</a></li>')
    return "\n".join(items)


def page(active: str, title: str, description: str, body: str) -> str:
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
  <div class="banner">Members-only preview for <strong>ProMedGen</strong> · Cardiovascular Precision Medicine Lab</div>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="index.html">
        <img src="assets/img/logo.png" alt="Shen Lab logo">
        <span class="brand-text">
          <strong>Shen Lab</strong>
          <span>Cardiovascular Precision Medicine</span>
        </span>
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav id="site-nav" aria-label="Primary">
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
      <div>
        <strong>Cardiovascular Precision Medicine Lab</strong>
        <p>Division of Cardiology · Center for Cardiovascular Research · Washington University School of Medicine in St. Louis</p>
        <small>Internal GitHub Pages site. Visible to people with read access to this repository. Not for public indexing.</small>
      </div>
      <div>
        <div class="affiliations">
          <img src="assets/img/washu-medicine.png" alt="WashU Medicine">
          <img src="assets/img/cvr-center.png" alt="Center for Cardiovascular Research">
        </div>
      </div>
    </div>
  </footer>
  <script src="js/site.js"></script>
</body>
</html>
"""


HOME = r"""
    <div class="wrap hero">
      <div>
        <p class="kicker">WashU Medicine · Cardiology</p>
        <h1>Human cells, CRISPR screens, and organoids for precision cardiovascular medicine.</h1>
        <p class="lede">The Cardiovascular Precision Medicine Lab is led by Dr. Mengcheng Shen, PhD. We decode the gene programs that drive congenital and acquired cardiovascular disease, then turn those maps into next-generation therapeutics.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="research.html">Research program</a>
          <a class="btn btn-ghost" href="models.html">Cell and organoid models</a>
        </div>
      </div>
      <div class="hero-media">
        <video autoplay muted loop playsinline poster="assets/img/cm-beating-poster.jpg">
          <source src="assets/video/cm-beating.mp4" type="video/mp4">
        </video>
        <img src="assets/img/cm-ctnt.jpg" alt="iPSC-cardiomyocytes stained for cardiac troponin T">
        <p class="caption">iPSC-cardiomyocytes · beating culture and cTnT (red), nuclei (blue)</p>
      </div>
    </div>

    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">Lab</p>
          <h2>What we do</h2>
        </div>
        <div class="prose">
          <p>The Cardiovascular Precision Medicine Lab is led by Dr. Mengcheng Shen, PhD, with a goal to understand the genetic and cellular mechanisms that regulate the development and function of the human cardiovascular system in health and disease. Using human induced pluripotent stem cells and emerging functional-genomic, genome-editing, and organoid technologies, we are focused on decoding the gene programs that drive congenital and acquired cardiovascular disease, the leading cause of death worldwide.</p>
          <p>To translate these findings back to the clinic, the lab also develops new approaches, including novel iPSC-cardiovascular models, high-throughput CRISPR screens, and single-cell Perturb-seq coupled with virtual-cell computational models, to nominate disease drivers and deliver next-generation, precision-based therapeutics, from small molecules that prevent anti-cancer drug–induced cardiotoxicity to chemically defined cells for regenerative medicine. By building these human-relevant models entirely from human cells, in step with the NIH New Approach Methodologies (NAMs) initiative, we ultimately seek to advance the diagnosis and treatment of cardiomyopathy, congenital heart disease, and related cardiovascular disorders.</p>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-head">
          <p class="kicker">Program</p>
          <h2>Five interconnected areas</h2>
          <p>The work spans differentiation, functional genomics, patient-specific disease models, precision cardio-oncology, and Perturb-seq for virtual-cell models.</p>
        </div>
        <div class="areas">
          <article class="area">
            <p class="mark">01 · Differentiation</p>
            <h3>Robust cardiovascular cells in 2D and 3D</h3>
            <p>Cardiomyocytes, endothelial cells, epicardial cells, smooth muscle cells, fibroblasts, pericytes, vessel organoids, and vascularized cardiac organoids — with xeno-free, chemically defined protocols.</p>
          </article>
          <article class="area">
            <p class="mark">02 · Functional genomics</p>
            <h3>Fate decisions and variant function</h3>
            <p>Genome-scale CRISPR screens, VUS knock-ins, and cell-type-specific tests of non-coding variants predicted to drive congenital heart disease.</p>
          </article>
          <article class="area">
            <p class="mark">03 · Disease modeling</p>
            <h3>Patient iPSCs with isogenic controls</h3>
            <p>Cardiomyopathy, pulmonary hypertension, and vascular disease, with druggable-genome screens that nominate drivers and rescue compounds.</p>
          </article>
          <article class="area">
            <p class="mark">04 · Cardio-oncology</p>
            <h3>Protect the heart without losing anti-cancer efficacy</h3>
            <p>Cancer-survivor iPSC cardiovascular cells plus CRISPR screens to reduce drug-induced cardiotoxicity.</p>
          </article>
          <article class="area">
            <p class="mark">05 · Perturb-seq</p>
            <h3>Training data for virtual cells</h3>
            <p>Physiologically relevant single-cell Perturb-seq in iPSC-derived cardiovascular cells for in silico foundation models.</p>
          </article>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <figure class="wide-figure">
          <img src="assets/img/research-overview.jpg" alt="Overview of Shen Lab research: iPSC differentiation, CRISPR screens, disease modeling, and cardio-oncology">
          <figcaption class="caption">Lab research overview · patient iPSCs, CRISPR editing, 2D/3D cardiovascular cell types, disease modeling, and cardio-oncology screens</figcaption>
        </figure>
      </div>
    </section>

    <section>
      <div class="wrap nams">
        <div>
          <p class="kicker">NAMs</p>
          <h2>Built on human-relevant methods</h2>
          <p>The program sits on the three pillars of the NIH New Approach Methodologies initiative: human in vitro models, human-relevant mechanism and safety, and in silico modeling.</p>
        </div>
        <ul>
          <li>hiPSC cardiovascular cells, vessel organoids, and multi-lineage cardiac organoids</li>
          <li>Patient-specific and isogenic models, VUS knock-ins, cardio-oncology safety screens</li>
          <li>Single-cell Perturb-seq and virtual-cell models</li>
        </ul>
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

    <section>
      <div class="wrap">
        <article class="pi">
          <img src="assets/img/headshot.jpg" alt="Portrait of Mengcheng Shen, PhD">
          <div>
            <p class="kicker">Principal investigator</p>
            <h2>Mengcheng Shen, PhD</h2>
            <p>Assistant Professor of Medicine and of Developmental Biology, Washington University School of Medicine. The lab uses high-throughput stem-cell and CRISPR-screen platforms to study genetic-variant and drug-induced cardiovascular pathologies.</p>
            <ul class="meta">
              <li>Cardiology</li>
              <li>Center for Cardiovascular Research</li>
              <li>Center of Regenerative Medicine</li>
              <li>Siteman Cancer Center</li>
            </ul>
            <a class="btn btn-ghost" href="people.html">Biography and links</a>
          </div>
        </article>
      </div>
    </section>
"""

RESEARCH = r"""
    <div class="wrap page-hero">
      <p class="kicker">Research</p>
      <h1>A human-cell pipeline from fate maps to therapeutics.</h1>
      <p class="lede">We integrate hiPSCs with CRISPR knockout, CRISPRi, and CRISPRa screens to define pathogenic drivers of congenital and acquired cardiovascular disease.</p>
    </div>

    <section>
      <div class="wrap stack">
        <article class="area">
          <p class="mark">01</p>
          <h2>Robust cardiovascular differentiation in 2D and 3D</h2>
          <p>We develop protocols to generate diverse cardiovascular cell types from hiPSCs — cardiomyocytes, endothelial cells, epicardial cells, cardiac neural crest cells, cardiac smooth muscle cells, cardiac fibroblasts, and cardiac pericytes — as well as vessel organoids and vascularized cardiac organoids. A current priority is engineering cardiac organoids that incorporate cardiomyocytes, vascular cells, and immune cells. To support regenerative medicine, we are establishing xeno-free, chemically defined protocols that perform reproducibly across diverse iPSC lines.</p>
        </article>
        <figure class="figure-card">
          <img src="assets/img/endothelial-protocol.jpg" alt="Xeno-free iPSC-endothelial cell differentiation protocol">
          <figcaption>High-efficiency iPSC-endothelial differentiation in a xeno-free system (CD144, CD31, eNOS, vWF).</figcaption>
        </figure>

        <article class="area">
          <p class="mark">02</p>
          <h2>Functional genomics for cell-fate decisions and variant function</h2>
          <p>We deploy genome-scale CRISPR screens to uncover master regulators of cell type–specific fate decisions. Using CRISPR genome editing, we install variants of uncertain significance into hiPSCs to resolve their pathophysiological consequences. We further apply deep-learning models to prioritize de novo non-coding variants predicted to drive congenital heart disease in a cell type–specific manner, then use CRISPR-edited iPSCs to establish genotype–phenotype causality.</p>
        </article>

        <article class="area">
          <p class="mark">03</p>
          <h2>Patient-specific disease modeling with isogenic controls</h2>
          <p>Using patient-derived hiPSCs paired with CRISPR/Cas9-corrected isogenic controls, we dissect cardiomyopathy, pulmonary hypertension, and vascular disease. Druggable-genome CRISPR screens nominate disease drivers without bias and identify small molecules that mitigate or rescue diseased phenotypes.</p>
        </article>

        <article class="area">
          <p class="mark">04</p>
          <h2>Precision cardio-oncology</h2>
          <p>We combine druggable-genome CRISPR screens with cancer survivors’ iPSC-derived cardiovascular cells to identify therapeutic targets that reduce anti-cancer drug-induced cardiovascular toxicity without compromising oncologic efficacy, a human-cell strategy aligned with the drug-safety goals of NAMs.</p>
        </article>
        <figure class="figure-card">
          <img src="assets/img/crispr-pipeline.jpg" alt="CRISPR screen pipeline for precision cardio-oncology">
          <figcaption>CRISPR screen pipeline in precision cardio-oncology: iPSC cardiovascular cells, anti-cancer drugs, deep sequencing, and compound rescue.</figcaption>
        </figure>
        <figure class="figure-card">
          <img src="assets/img/cardio-oncology.jpg" alt="Illustration of the heart and tumor cells for cardio-oncology">
          <figcaption>Cardio-oncology: protect cardiovascular tissue during anti-cancer therapy.</figcaption>
        </figure>

        <article class="area">
          <p class="mark">05</p>
          <h2>Single-cell Perturb-seq for virtual-cell foundation models</h2>
          <p>We are generating physiologically relevant single-cell Perturb-seq datasets in iPSC-derived cardiovascular cells to train virtual-cell foundation models, advancing scalable in silico approaches to cardiovascular research.</p>
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

    <section>
      <div class="wrap">
        <h2>Selected references</h2>
        <ol class="refs">
          <li>Takahashi K, et al. Induction of pluripotent stem cells from adult human fibroblasts by defined factors. <em>Cell</em>. 2007.</li>
          <li>Lian X, et al. Robust cardiomyocyte differentiation from human pluripotent stem cells via temporal modulation of canonical Wnt signaling. <em>PNAS</em>. 2012.</li>
          <li>Burridge PW, et al. Chemically defined generation of human cardiomyocytes. <em>Nat Methods</em>. 2014.</li>
          <li>Wimmer RA, et al. Human blood vessel organoids as a model of diabetic vasculopathy. <em>Nature</em>. 2019.</li>
          <li>Hofbauer P, et al. Cardioids reveal self-organizing principles of human cardiogenesis. <em>Cell</em>. 2021.</li>
          <li>Dixit A, et al. Perturb-Seq: dissecting molecular circuits with scalable single-cell RNA profiling of pooled genetic screens. <em>Cell</em>. 2016.</li>
          <li>Replogle JM, et al. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. <em>Cell</em>. 2022.</li>
          <li>National Institutes of Health. NIH to Prioritize Human-Based Research Technologies. April 29, 2025.</li>
          <li>NIH Common Fund. <a href="https://commonfund.nih.gov/complementarie">Complement-ARIE</a>.</li>
          <li>U.S. Food and Drug Administration. Roadmap to Reducing Animal Testing in Preclinical Safety Studies. April 2025.</li>
        </ol>
      </div>
    </section>
"""

MODELS = r"""
    <div class="wrap page-hero">
      <p class="kicker">Models</p>
      <h1>A cardiovascular cell atlas grown from hiPSCs.</h1>
      <p class="lede">2D lineages, engineered heart tissues, vessel organoids, and vascularized cardiac organoids, plus the rooms where the work happens.</p>
    </div>

    <section>
      <div class="wrap">
        <h2>Beating cells and tissues</h2>
        <div class="gallery">
          <figure class="figure-card">
            <video controls playsinline poster="assets/img/cm-beating-poster.jpg">
              <source src="assets/video/cm-beating.mp4" type="video/mp4">
            </video>
            <figcaption>iPSC-cardiomyocytes, brightfield beating culture.</figcaption>
          </figure>
          <figure class="figure-card">
            <video controls playsinline>
              <source src="assets/video/cm-myl7.mp4" type="video/mp4">
            </video>
            <figcaption>iPSC-cardiomyocytes, MYL7 (green) beating reporter.</figcaption>
          </figure>
          <figure class="figure-card">
            <video controls playsinline>
              <source src="assets/video/eht-brightfield.mp4" type="video/mp4">
            </video>
            <figcaption>iPSC-engineered heart tissues, brightfield.</figcaption>
          </figure>
          <figure class="figure-card">
            <video controls playsinline>
              <source src="assets/video/eht-myl7.mp4" type="video/mp4">
            </video>
            <figcaption>iPSC-engineered heart tissues, MYL7-eGFP.</figcaption>
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
            <video controls playsinline poster="assets/img/cardiac-organoid-poster.jpg">
              <source src="assets/video/cardiac-organoids.mp4" type="video/mp4">
            </video>
            <figcaption>iPSC-cardiac organoids.</figcaption>
          </figure>
          <figure class="figure-card">
            <video controls playsinline>
              <source src="assets/video/vascularized-organoids.mp4" type="video/mp4">
            </video>
            <figcaption>iPSC-vascularized cardiac organoids.</figcaption>
          </figure>
          <figure class="figure-card">
            <img src="assets/img/vessel-organoid.jpg" alt="iPSC vessel organoid stained for DAPI, VE-cadherin, CD31, PDGFRβ">
            <figcaption>iPSC-vessel organoid · DAPI | VE-cadherin | CD31 | PDGFRβ.</figcaption>
          </figure>
          <figure class="figure-card">
            <video controls playsinline>
              <source src="assets/video/vessel-organoids.mp4" type="video/mp4">
            </video>
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
            <video controls playsinline poster="assets/img/lab-space.jpg">
              <source src="assets/video/lab-space.mp4" type="video/mp4">
            </video>
            <figcaption>Laboratory space.</figcaption>
          </figure>
          <figure class="figure-card">
            <video controls playsinline poster="assets/img/tissue-culture.jpg">
              <source src="assets/video/tissue-culture.mp4" type="video/mp4">
            </video>
            <figcaption>Tissue culture room.</figcaption>
          </figure>
        </div>
      </div>
    </section>
"""

PEOPLE = r"""
    <div class="wrap page-hero">
      <p class="kicker">People</p>
      <h1>Mengcheng Shen, PhD</h1>
      <p class="lede">Assistant Professor of Medicine · Assistant Professor of Developmental Biology · Washington University School of Medicine</p>
    </div>

    <section>
      <div class="wrap">
        <article class="pi">
          <img src="assets/img/headshot.jpg" alt="Portrait of Mengcheng Shen, PhD">
          <div>
            <p>The lab is led by Dr. Mengcheng Shen. His research uses high-throughput stem-cell and CRISPR-screen platforms to study novel genetic-variant and drug-induced cardiovascular pathologies, with the aim of advancing precision cardiovascular medicine.</p>
            <ul class="meta">
              <li>Division of Cardiology</li>
              <li>Center for Cardiovascular Research</li>
              <li>Center of Regenerative Medicine</li>
              <li>Siteman Cancer Center</li>
              <li>ICTS</li>
            </ul>
            <p>DBBS programs: Developmental, Regenerative and Stem Cell Biology; Immunology; Molecular Cell Biology; Molecular Genetics and Genomics; Neurosciences.</p>
          </div>
        </article>
      </div>
    </section>

    <section>
      <div class="wrap prose">
        <h2>Training</h2>
        <ul>
          <li>BSc, Nanjing Agricultural University, 2009</li>
          <li>MSc, Nanjing Agricultural University, 2012</li>
          <li>PhD, University of Alberta, 2018</li>
        </ul>
        <h2>Selected recognition</h2>
        <ul>
          <li>Best Poster Award, Stanford Bio-X Interdisciplinary Initiatives Seed Grants Program, 2024</li>
          <li>Best Poster Award, Stanford–Weill Cornell Cardiovascular Research Symposium, 2022</li>
          <li>Peter Pang Best Ph.D. Thesis Award, University of Alberta, 2018</li>
          <li>Med Star Publication Award for Graduate Student, 2018</li>
          <li>Dr. Francis X. Witkowski Publication Award, 2018</li>
        </ul>
        <h2>Profiles</h2>
        <ul class="contact-list">
          <li><a href="https://cardiology.wustl.edu/people/mengcheng-shen-phd/">WashU Cardiology faculty page</a></li>
          <li><a href="https://profiles.wustl.edu/en/persons/mengcheng-shen">WashU Research Profile</a></li>
          <li><a href="https://orcid.org/0000-0001-7037-6159">ORCID 0000-0001-7037-6159</a></li>
        </ul>
      </div>
    </section>
"""

JOIN = r"""
    <div class="wrap page-hero">
      <p class="kicker">Join</p>
      <h1>Human cardiovascular biology, at the resolution of a CRISPR screen.</h1>
      <p class="lede">The lab is building iPSC models, organoids, and Perturb-seq datasets for precision cardio-oncology and regenerative medicine. Trainees interested in those problems are welcome to reach out.</p>
    </div>

    <section>
      <div class="wrap prose">
        <h2>Who we are looking for</h2>
        <p>Dr. Shen is listed as willing to mentor PhD and MSTP students. We are especially interested in people who want to work at the intersection of stem-cell models, functional genomics, and cardiovascular disease.</p>
        <h2>How to inquire</h2>
        <p>Use the WashU faculty profile to start a conversation. Do not send unpublished patient data to this GitHub repository.</p>
        <ul class="contact-list">
          <li><a href="https://cardiology.wustl.edu/people/mengcheng-shen-phd/">cardiology.wustl.edu/people/mengcheng-shen-phd</a></li>
          <li><a href="https://profiles.wustl.edu/en/persons/mengcheng-shen">profiles.wustl.edu/en/persons/mengcheng-shen</a></li>
        </ul>
        <h2>Affiliations</h2>
        <div class="affiliations">
          <img src="assets/img/washu-medicine.png" alt="WashU Medicine">
          <img src="assets/img/cvr-center.png" alt="Center for Cardiovascular Research">
        </div>
      </div>
    </section>
"""


def main() -> None:
    pages = {
        "index.html": (
            "Shen Lab · Cardiovascular Precision Medicine",
            "Cardiovascular Precision Medicine Lab at WashU Medicine, led by Mengcheng Shen, PhD.",
            HOME,
        ),
        "research.html": (
            "Research · Shen Lab",
            "Five research areas of the Shen Lab: differentiation, CRISPR screens, disease modeling, cardio-oncology, and Perturb-seq.",
            RESEARCH,
        ),
        "models.html": (
            "Models · Shen Lab",
            "iPSC-derived cardiovascular cell types, organoids, engineered heart tissues, and lab spaces.",
            MODELS,
        ),
        "people.html": (
            "People · Shen Lab",
            "Mengcheng Shen, PhD, principal investigator of the Cardiovascular Precision Medicine Lab.",
            PEOPLE,
        ),
        "join.html": (
            "Join · Shen Lab",
            "Join the Cardiovascular Precision Medicine Lab at Washington University School of Medicine.",
            JOIN,
        ),
    }
    for name, (title, desc, body) in pages.items():
        (ROOT / name).write_text(page(name, title, desc, body), encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()

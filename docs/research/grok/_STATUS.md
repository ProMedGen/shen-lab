# Theme-figure research — status

**Status: Partial.** Verified visual language is usable. The original eight-file
deliverable is now on disk, but several numbered items from
`docs/research/theme_figure_research_prompts.md` were not independently
verified (ten-item figure catalogs, some tropes, two vendor-published
filled 2K prompts).

## What ran

Host workflow `deep-research` (display name), ~12.5 min.

- Planner collapsed RQ1–RQ8 into **4** research questions (workflow cap).
- Four researchers, **6 claims each** (24 candidates).
- Two independent verifiers: **22 of 24** claims retained.
- Synthesizer wrote a cited report. Agents were **read-only**, so nothing
  was written into this folder until this follow-up.

## Files in this folder

| File | Role |
| --- | --- |
| `SYNTHESIS.md` | Combined verified answer + ranked 16:9 blueprints + sources |
| `RQ1_ipsc.md` | iPSC identity and directed cardiogenesis |
| `RQ2_devbio.md` | Heart morphogenesis, organoids, gastruloids |
| `RQ3_crispr.md` | CRISPR / CRISPRi/a screens without scissors |
| `RQ4_multiomics.md` | Perturb-seq / single-cell (thin; one claim rejected) |
| `RQ5_ml.md` | Virtual-cell and lab-in-the-loop metaphors |
| `RQ6_cardioonc.md` | Cardio-oncology as sequence and balance |
| `RQ7_integration.md` | Three ranked 16:9 hero blueprints |
| `RQ8_promptcraft.md` | Vendor prompt rules + a constructed 2K template |

## Claims excluded by verification

1. **Droplet = CBC + UMI + guide barcode as a class.** Drop-seq shows
   cell + barcoded bead with PCR handle, cell barcode, UMI, oligo-dT.
   Guide/perturbation barcodes appear only in Perturb-seq / 10x capture
   papers. Do not draw a three-index droplet as the default scRNA glyph.
2. **Current `research-themes.jpg` is a CSS-cropped hero.** It is a dark
   six-theme hub-and-spoke image in `.theme-figure` (`width:100%;
   height:auto`). `object-fit:cover` and the bottom-weighted gradient
   apply to `banner-home.jpg`, not this schematic.

## Hard gaps (do not treat as findings)

- No journal style bible for iPSC / sarcomere / organoid palettes.
- Ten-item figure/cover lists per RQ were not fully open-image verified
  (paywalls). Partial catalogs below use only inspected sources.
- Hofbauer et al., Cell 2021 cardioids: not retrieved as a standalone claim.
- Variant knock-in (VUS HDR) illustration conventions: not inspected.
- Arrayed-versus-pooled plate drawings on Cell/Nature/Science covers: not inspected.
- Bunne et al., Cell 2024 virtual-cell figure pixels: not inspected.
- Vendor pages do not name “symmetric-icon syndrome” or “love-heart prior.”
- Vendor pages do not publish two filled text-free 2K Nature/Science-cover
  scientific-scene prompts. RQ8 examples are **constructed** from verified
  vendor rules plus verified biology shapes.

## How to use this packet

1. Draw from `RQ7_integration.md` blueprint **1** (concentric doughnut).
2. Generate with `RQ8_promptcraft.md` example 1 at native **16:9 / 2K**.
3. Keep CRISPR, ML, and cardio-oncology as secondary grammar (blueprint 3),
   not as six icons around a cartoon heart.
4. Add all type in post. Keep the generated frame text-free.

# RQ3 — Visual language of CRISPR functional genomics and screens

**Status: Partial.** Structure vs scissors, pooled-screen flow, and
bidirectional CRISPRi/a arms are verified. Variant knock-in (VUS HDR)
conventions and a ten-item CRISPR-cover census were not inspected.

## 1. Element inventory

| Element | Drawable form in inspected sources | Not this |
| --- | --- | --- |
| Cas9 complex | **Bilobed protein (REC + NUC)** wrapping a **T-shaped sgRNA:DNA heteroduplex** in a positively charged groove. Ribbon, surface, or electrostatic map (Nishimasu et al., Cell 2014). | Scissors glyph; “cutting device.” |
| dCas9 CRISPRi/a | Protein seated on a DNA loop (lab `crispr-pipeline.jpg`); two **parallel fusion arms**. | Helix-plus-scissors (lab `research-themes.jpg`, dated). |
| Guide library | Oligo / sgRNA pool entering cells at **low MOI so one guide per cell**. | A volcano plot inside the schematic. |
| Arrayed vs pooled plates | Defined in prose (Dixit). Pooled lentiviral workflows are drawn (Gilbert; Liu/Shen). | No inspected Cell/Nature/Science **cover** with a side-by-side multiwell vs mixed-pool drawing. |
| Enrichment / depletion | **Surviving-cell stream** after selection or toxin; NGS of sgRNA barcodes. | Axes, scatter, or fake data in the hero. |

Pooled-screen left-to-right flow (Gilbert Fig. 1A; Liu/Shen Fig. 1A):

1. Oligo / sgRNA library
2. Low-MOI infection (Liu/Shen: MOI 0.3, one guide per iCM)
3. Selection (puromycin) and/or toxin (doxorubicin vs vehicle)
4. Harvest of survivors
5. NGS of sgRNA barcodes

Scatter plots of hits live in **separate data panels**, not inside the
workflow drawing.

## 2. Bidirectional CRISPRi / CRISPRa

Verified metaphor: **two parallel dCas9 fusion arms**, not a dimmer switch
(dimmer-switch art was requested; not found in inspected pages).

- CRISPRi: dCas9-**KRAB** repressor; guides just **downstream** of the TSS.
- CRISPRa: dCas9-**VP64 / SunTag / VPR**; guides peak about **−400 to −50 bp**
  of the TSS.
- Phenotypes are **anti-correlated**, ~1000-fold range on the same genes
  (Gilbert Fig. 3C–E).
- Liu/Shen run KRAB and VPR as **separate pooled arms** on the same
  iCM / doxorubicin survival design.

## 3. Dramatizing a hit without a volcano

Gilbert Fig. 6B maps hits as **protein-complex / pathway circles**
(protective versus sensitizing). That is the inspected non-volcano hit
graphic.

Do not put a volcano, bar chart, or labeled UMAP in the hero.

## 4. Inspected figures (partial catalog)

| Source | One-line lesson |
| --- | --- |
| Nishimasu et al., Cell 2014, Figs. 1 and 4 | Current Cas9 = bilobed protein + T-shaped heteroduplex, not scissors. |
| NIGMS Image Gallery 7036 | Dated education art: locate, cut, repair “cutting device.” Do not copy. |
| Lab `research-themes.jpg` | Helix + scissors for “functional genomics”: the thing to retire. |
| Lab `crispr-pipeline.jpg` | dCas9-like protein on a CRISPRi/a DNA loop: the language to keep. |
| Gilbert et al., Cell 2014, Fig. 1A | Pooled screen = left-to-right process, not a chart. |
| Gilbert et al., Fig. 3A, 3C–E | CRISPRa = SunTag-VP64 arm; anti-correlated with CRISPRi. |
| Gilbert et al., Fig. 6B | Hits as pathway circles (protective vs sensitizing). |
| Liu, Shen et al., Cell Stem Cell 2024, Fig. 1A–C | iCM CRISPRi/a + doxorubicin: lab’s own screen grammar. |
| Science 365(6452) cover, 2 Aug 2019 | CRISPR special-issue cover was a **photo of an edited tomato seedling**, not a Cas9 cartoon. |

Inspected Nature/Science CRISPR covers in this pass are that tomato photo,
not an inventory of ten screen covers.

## 5. DO / DON’T

**DO**

- Bilobed Cas9 or a dCas9 protein on DNA.
- Parallel KRAB vs VPR arms for bidirectional screens.
- Left-to-right surviving-cell stream into NGS barcodes.
- Pathway circles for hits.

**DON’T**

- 2015-era scissors clipart / helix-plus-scissors.
- Volcano or scatter inside the schematic.
- Named “cutting device” education sequences.
- Fake axes or readable gene names on a type-free hero.
- Assume VUS knock-in has a canonical cover glyph (not inspected).

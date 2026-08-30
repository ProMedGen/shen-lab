# Shen Lab hero theme candidates — v8 (theme-matched BioRender icons)

Round 6. The v7 BioRender style was approved in principle, but its icon
set didn't map to the lab's six research themes (it had a generic
organoid icon and no cardio-oncology icon) and left no room for captions.
Both v8 tasks ran via `production/shen_lab_theme/queue.json` (model:
Gemini 3.1 "Nano Banana 2", 2K, 16:9, maxCredits 0 — both measured 0
credits, no regeneration retries needed) on the **`methods`** Firefly
lane (never the shared default profile), per the standing lane
instruction.

Each image has exactly six icons mapping 1:1 to the lab's six research
themes, in this fixed order: **iPSC** (petri dish + colony) →
**developmental biology** (crescent + tube pair) → **functional
genomics** (DNA helix + protein) → **multiomics** (stacked diamonds) →
**machine learning** (monitor with dots) → **cardio-oncology** (capsule +
cardiac muscle cell).

**QC criteria (simplicity is the goal):**
- Hard fail: rendered text/letters; photorealistic or 3D look; dark
  background; glow; clutter; not exactly six icons; missing the
  capsule/medicine icon; cartoon love-heart; scissors.
- Pass requires: clean white background, flat vector icons with thin
  outlines, all six icons present and similar in size, clear empty white
  space reserved for captions, instantly readable like a talk slide.

| Filename | Layout | QC verdict |
| --- | --- | --- |
| `shen-theme-biorender-row-v8.jpg` | Six icons in a horizontal row connected by thin arrows, in theme order left→right, with a clear light empty band reserved across the lower third for captions | **PASSES.** Clean white background, exactly six consistently-sized flat vector icons with thin outlines and single flat tones, correct theme mapping including the required capsule/medicine icon for cardio-oncology, generous white/light-gray reserved space below the icon row for captions. No text, no 3D/photorealistic rendering, no dark background, no glow, no clutter, no heart, no scissors. |
| `shen-theme-biorender-cycle-v8.jpg` | Same six icons arranged clockwise around a circular arrow loop starting at 12 o'clock (iPSC) through developmental biology, functional genomics, multiomics, machine learning, and cardio-oncology back to iPSC, with the ring's center and side margins left empty | **PASSES.** Clean white background, exactly six consistently-sized flat vector icons with thin outlines and single flat tones, correct theme mapping including the capsule/medicine icon, wide left/right margins and an empty circle center reserved for a caption/title. No text, no 3D/photorealistic rendering, no dark background, no glow, no clutter, no heart, no scissors. |

## Icon-center pixel coordinates (2560×1440 frame)

Coordinates were determined programmatically (Python + PIL/NumPy/SciPy,
not eyeballed) from the native-resolution source images (2048×1143),
then scaled to the requested 2560×1440 frame. Row-image icons were
located via wide contiguous non-white column runs (thin arrow columns
discarded); cycle-image icons were located via connected-component
centroids of the six largest non-white blobs (thin arrow arcs discarded
by area), ordered clockwise starting at the 12 o'clock component.

**`shen-theme-biorender-row-v8.jpg`** (all six icons sit at roughly the same height, y ≈ 687–702, leaving the lower third clear for captions):

| # | Theme | x | y |
| --- | --- | --- | --- |
| 1 | iPSC (petri dish + colony) | 269 | 702 |
| 2 | Developmental biology (crescent + tube pair) | 628 | 702 |
| 3 | Functional genomics (DNA helix + protein) | 1088 | 692 |
| 4 | Multiomics (stacked diamonds) | 1479 | 702 |
| 5 | Machine learning (monitor with dots) | 1893 | 691 |
| 6 | Cardio-oncology (capsule + cardiac muscle cell) | 2316 | 687 |

**`shen-theme-biorender-cycle-v8.jpg`** (ring center ≈ (1280, 720) is empty and reserved for a title/caption):

| # | Theme | x | y |
| --- | --- | --- | --- |
| 1 | iPSC (petri dish + colony) — top | 1280 | 231 |
| 2 | Developmental biology (crescent + tube pair) — upper right | 1783 | 491 |
| 3 | Functional genomics (DNA helix + protein) — lower right | 1717 | 951 |
| 4 | Multiomics (stacked diamonds) — bottom | 1280 | 1216 |
| 5 | Machine learning (monitor with dots) — lower left | 848 | 950 |
| 6 | Cardio-oncology (capsule + cardiac muscle cell) — upper left | 858 | 527 |

## Regeneration notes
- Both tasks generated cleanly on the first pass — zero hard fails, zero regeneration retries needed.
- Run budget: 0 credits spent (guard-verified `cost=0` on every task before submission).
- Source files: `output/images/<task-id>_var1.webp` in the FireFly repo (native resolution 2048×1143); these JPGs are 92%-quality re-encodes for review/commit into this repo.
- Prior rounds (`theme_candidates_v3/` through `theme_candidates_v7/`) remain in the repo for comparison; the corresponding v3–v7 queue tasks are now disabled in favor of this v8 theme-matched round.

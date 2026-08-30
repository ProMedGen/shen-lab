# Shen Lab hero theme candidates — v7 (simple BioRender-style schematic)

Round 5. The owner rejected every elaborate render from rounds v3–v6 —
they want a SIMPLE BioRender-style schematic instead: flat vector icons,
clean white background, instantly readable like a talk slide. Both tasks
ran via `production/shen_lab_theme/queue.json` (model: Gemini 3.1 "Nano
Banana 2", 2K, 16:9, maxCredits 0 — both measured 0 credits, no
regeneration retries needed) on the **`methods`** Firefly lane (never the
shared default profile), per the standing lane instruction.

**QC criteria this round are inverted from prior rounds** — simplicity is
the goal, not biological texture or drama.

- **Hard fail:** rendered text/letters; photorealistic or 3D-rendered
  look; dark background; glowing effects; dense microscopy texture;
  cluttered composition; missing icons (must be six); cartoon
  love-heart; scissors.
- **Pass requires:** clean white background, flat vector icons with thin
  outlines and one flat tone each, consistent icon size, clear white
  space, instantly readable at a glance like a talk slide.

| Filename | Style intent | QC verdict |
| --- | --- | --- |
| `shen-theme-biorender-row-v7.jpg` | Six flat icons in a horizontal row connected by thin arrows: petri dish with iPSC cell cluster → striated muscle fiber bundles → vascularized organoid disc → DNA helix with variant marker → three stacked data layers → laptop/monitor readout | **PASSES — reads as a simple BioRender-style slide diagram.** Clean white background, exactly six consistently-sized flat vector icons with thin outlines and clear single-tone fills, generous white space, thin connecting arrows between each step, instantly legible workflow at a glance. No text, no 3D/photorealistic rendering, no dark background, no glow, no microscopy texture, no clutter, no heart, no scissors. |
| `shen-theme-biorender-cycle-v7.jpg` | Same six icons arranged evenly around a circular arrow loop (petri dish top, proceeding clockwise through muscle fibers, organoid disc, DNA helix, data layers, monitor, back to petri dish) | **PASSES — reads as a simple BioRender-style slide diagram.** Clean white background, exactly six consistently-sized flat vector icons with thin outlines and single-tone fills, generous white space in the center and around the ring, thin circular arrow path linking all six steps in sequence, instantly legible closed-loop workflow at a glance. No text, no 3D/photorealistic rendering, no dark background, no glow, no microscopy texture, no clutter, no heart, no scissors. |

## Regeneration notes
- Both tasks generated cleanly on the first pass — zero hard fails, zero regeneration retries needed.
- Run budget: 0 credits spent (guard-verified `cost=0` on every task before submission).
- Source files: `output/images/<task-id>_var1.webp` in the FireFly repo; these JPGs are 92%-quality re-encodes for review/commit into this repo.
- Prior rounds (`theme_candidates_v3/` through `theme_candidates_v6/`) remain in the repo for comparison; the corresponding v3–v6 queue tasks are now disabled in favor of this v7 simple-schematic round.

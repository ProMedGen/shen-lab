# Shen Lab hero theme candidates — v3

Generated via `production/shen_lab_theme/queue.json` (model: Gemini 3.1
"Nano Banana 2", 2K, 16:9, maxCredits 0 — all four ran at 0 measured
credits). Blueprints referenced below are from
`docs/research/grok/RQ7_integration.md`.

| Filename | Style / blueprint | QC verdict |
| --- | --- | --- |
| `shen-theme-organoid-photo-v3.jpg` | Blueprint 1 — concentric vascularized-cardiac-organoid doughnut, dark editorial **photograph** treatment (low-angle, shallow DOF, rim light) | PASS. No text/pseudo-text, no heart silhouette (clean torus geometry), no scissors, no red anywhere (palette is green/orange/cyan on navy), no chart axes or neural-net diagram, not a bland blob — visible layered structure (cell rim, striated green ring, branching orange vessel plexus, cyan core) plus the faint crescent→bud background motif called for in the prompt. Reads well as a lab hero image. |
| `shen-theme-organoid-illus-v3.jpg` | Blueprint 1 — same doughnut geometry, premium dark **illustration** treatment (flatter, cleaner linework, soft inner luminescence) | PASS. Same clean checks as above (no text, no heart, no red, no scissors, no diagram/axes). Slightly more graphic/illustrative than the photo variant, good contrast pair for A/B with it. |
| `shen-theme-tokenfield-v3.jpg` | Blueprint 2 — split scene: left dark navy virtual-cell token lattice with one token expanding into the organoid doughnut; right lighter warm-grey field, one biological cell resting on copper circuit traces feeding into the lattice | PASS, with a minor note. No text, no heart silhouette, no red, no scissors, no perceptron/point-cloud diagram. The right-side "cell on circuit traces" reads a touch more like a smooth pebble/rock than an obviously biological cell with a distinct nucleus — acceptable but the weakest match to intent of the four; still usable as the Blueprint 2 (virtual-cell / multiomic) candidate. |
| `shen-theme-organoid-light-v3.jpg` | Blueprint 1 — flat light editorial variant (off-white background, thin uniform outlines, flat single-tone fills, leaf-green/apricot-orange/soft-cyan palette) | PASS, with a minor note. No text, no heart silhouette, no red, no scissors, no arrows/chart axes, not a bland blob. Geometry differs slightly from the two dark doughnut variants: it renders as a filled disc with an off-center cyan core rather than a true center-hole torus, so it reads more like a "target/orbit" motif than a doughnut — still a clean, textbook-quality light editorial illustration and a reasonable stand-alone light-mode candidate, but note the geometry mismatch if strict visual consistency with the dark doughnut pair is required.

## Regeneration notes
- All four tasks generated cleanly on the first pass (no HARD FAILs, no re-runs needed).
- Run budget: 0 credits spent (guard-verified `cost=0` on every task before submission).
- Source files: `output/images/<task-id>_var1.{webp,png}` in the FireFly repo; these JPGs are 92%-quality re-encodes for review/commit into this repo.

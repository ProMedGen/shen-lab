# Shen Lab hero theme candidates — v4

Round 2, generated after owner review of the v3 set. All five tasks ran
via `production/shen_lab_theme/queue.json` (model: Gemini 3.1 "Nano
Banana 2", 2K, 16:9, maxCredits 0 — all five measured 0 credits, no
regeneration needed, no hard fails).

| Filename | Style intent | QC verdict |
| --- | --- | --- |
| `shen-theme-organoid-micro-v4.jpg` | Authentic fluorescence-microscopy voice: organoid on true black, self-emitting emerald ring, orange vessel network, cyan core, faint out-of-focus neighbor specimen upper left | PASS. No text/pseudo-text, no heart silhouette, no red, no scissors, no arrows, no chart axes. Reads convincingly as a real wide-field fluorescence micrograph rather than a 3D render — strongest "authentic imaging" candidate of the round. |
| `shen-theme-organoid-cine-v4.jpg` | Cinematic three-plane scene: background bokeh, mid-ground pale crescent→bud→tube embryonic sequence, foreground/main-subject organoid on the right golden-ratio line with a volumetric light shaft | PASS. No text, no heart, no red, no scissors, no arrows, no chart axes. Depth staging across the three planes reads clearly and gives a strong narrative "story in depth" feel, good match to intent. |
| `shen-theme-eclipse-v4.jpg` | Eclipse-corona editorial cover metaphor: dark tissue disc, blazing orange-gold vessel corona radiating outward like solar prominences, thin green muscle band, small cyan coiled core at center | PASS. No text, no heart silhouette, no red, no scissors, no chart axes, no arrows. Bold, iconic, single-metaphor cover language — the most visually striking candidate; ring is intentionally circular/symmetric per the eclipse metaphor, not a heart shape. |
| `shen-theme-tokenfield-dark-v4.jpg` | All-dark token field (no light half): continuous navy field, dim oval token lattice, one token awakened into the organoid, copper circuit traces entering from the right edge and terminating in glowing pads near the ring | PASS. No text, no heart, no red, no scissors, no arrows, no chart axes, and confirmed no light-half split — successfully addresses the "all-dark" correction from the v3 split-scene version. |
| `shen-theme-organoid-light-v4.jpg` | Corrected light flat editorial: true open ring (doughnut) with a genuinely empty white hole holding only the small cyan core, green muscle band, orange vessel branches, beaded cell rim, quiet crescent/bud vignette upper left | PASS. No text, no heart, no red, no scissors, no chart axes, and critically **no arrows** and **no filled disc** — the center hole is clearly open background color, successfully fixing the v3 light variant's filled-disc/geometry mismatch. |

## Regeneration notes
- All five tasks generated cleanly on the first pass — zero HARD FAILs, zero regeneration retries needed.
- Run budget: 0 credits spent (guard-verified `cost=0` on every task before submission).
- Source files: `output/images/<task-id>_var1.webp` in the FireFly repo; these JPGs are 92%-quality re-encodes for review/commit into this repo.
- The v3 candidates (`docs/research/theme_candidates_v3/`) remain in the repo for comparison; the corresponding v3 queue tasks are now disabled in favor of this v4 round.

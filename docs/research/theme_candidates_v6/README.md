# Shen Lab hero theme candidates — v6 (biology-honest, anti-jade)

Round 4. A professional reviewer hard-failed every prior round (v3–v5) as
"carved jade pendants" — smooth, polished solid objects rather than real
biology. The prompts were rewritten texture-first for this round. Both
tasks ran via `production/shen_lab_theme/queue.json` (model: Gemini 3.1
"Nano Banana 2", 2K, 16:9, maxCredits 0 — both measured 0 credits, no
regeneration retries needed).

Generated on the **`methods`** Firefly lane (not the shared default
profile), per owner instruction to keep this Shen Lab work off the
default Chrome profile used by other concurrent agents.

**Ground-truth reference used for QC:** `assets/img/vascularized-organoids-poster.jpg`
(real confocal 3D-reconstruction of a vascularized cardiac organoid —
chaotic anastomosing green vessel web threading through irregular red
tissue chunks, visibly granular, fuzzy interdigitating zone boundaries,
nothing smooth or polished). `real-imagery-mock.jpg` in this folder is a
pre-existing reference/mock and was left untouched.

**Anti-jade hard-fail criteria applied:** rendered text/letters; smooth
polished jade/ceramic-looking solid torus; any coiled rope/spiral core;
thick smooth symmetric tube trees; cartoon love-heart silhouette. Tissue
must look granular/multicellular with fuzzy zone edges; vessels must form
a chaotic anastomosing web (not a clean radiating tree).

| Filename | Style intent | QC verdict (anti-jade test) |
| --- | --- | --- |
| `shen-theme-confocal-v6.jpg` | Stitched top-down confocal fluorescence micrograph of a circular micropatterned stem-cell colony: true black background, granular multicellular texture, patchy uneven green reporter zone, orange-gold capillary web, dim cyan spindle-cell core, ragged outer margin | **PASSES the anti-jade test explicitly.** Visibly granular/multicellular throughout (individual nuclei resolvable as grain), green zone is patchy with fuzzy, interdigitating edges (not a clean ring), vessels form a genuinely chaotic anastomosing web with irregular branching and loops closely mirroring the real reference image. No text, no polished torus, no coiled rope core, no smooth symmetric tube tree, no heart silhouette. Strongest "real biology" candidate of all four rounds. |
| `shen-theme-volume-v6.jpg` | Scientific 3D volume-rendering (research-visualization-software aesthetic) of an irregular, asymmetric, lobed vascularized cardiac organoid on a dark charcoal viewport, with a dense chaotic vessel web penetrating the tissue and one lobe optically clipped open | **PASSES the anti-jade test.** Silhouette is irregular/lobed, not a symmetric torus; surface carries visible granular speckle (not glossy/polished); vessels branch, loop, and reconnect across and into the tissue forming a real web rather than a simple radiating tree; cyan appears only as short mural sleeve segments, no coiled rope. Slightly smoother-surfaced and less extremely fractal than the confocal sibling image and the ground-truth reference, but none of the explicit hard-fail bans (jade torus, coiled spiral, smooth symmetric tree, text, heart) are triggered. |

## Regeneration notes
- Both tasks generated cleanly on the first pass — zero hard fails, zero regeneration retries needed.
- Run budget: 0 credits spent (guard-verified `cost=0` on every task before submission).
- Source files: `output/images/<task-id>_var1.webp` in the FireFly repo; these JPGs are 92%-quality re-encodes for review/commit into this repo.
- Prior rounds (`theme_candidates_v3/`, `theme_candidates_v4/`, `theme_candidates_v5/`) remain in the repo for comparison; the corresponding v3–v5 queue tasks are now disabled in favor of this v6 biology-honest round.

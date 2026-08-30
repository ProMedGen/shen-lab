# Shen Lab hero theme candidates — v5 (NEJM review-figure style)

Round 3, generated after owner request for a true NEJM (New England
Journal of Medicine) review-article illustration voice, reverse-engineered
into a dedicated style block. Both tasks ran via
`production/shen_lab_theme/queue.json` (model: Gemini 3.1 "Nano Banana 2",
2K, 16:9, maxCredits 0 — both measured 0 credits, no regeneration needed,
no hard fails).

**Style intent (shared by both images):** NEJM review-figure voice — soft
airbrushed gradient-mesh shading, no hard outlines anywhere (forms
modeled purely by tonal shifts), muted naturalistic clinical palette only
(sage green, warm terracotta tan, slate blue, dusty rose, cream — nothing
neon or fully saturated, no pure black), one soft diffuse light from the
upper left, clean white background with generous margins, calm precise
educational clinical-textbook tone. Explicitly no dark background, no
glow/bloom, no rim light, no film grain.

| Filename | Style intent (task-specific) | QC verdict |
| --- | --- | --- |
| `shen-theme-nejm-organoid-v5.jpg` | Single organoid subject on white: open-ring vascularized cardiac organoid (sage-green muscle band, terracotta vessel tree, slate-blue/dusty-rose coiled core in the open white hole, beaded cream outer rim) with a small pale companion crescent→bud vignette upper left | PASS. Clean white background (not dark), no hard black outlines (all forms softly tonally modeled), no neon/saturated colors, no glow/bloom effects, no text/pseudo-text, no heart silhouette, no scissors, no chart axes, no arrows. True open ring — center hole is genuine white space around the core, not a filled disc. Excellent match to the classic medical-journal review-illustration voice. |
| `shen-theme-nejm-scene-v5.jpg` | Organoid plus two circular zoom insets: same open-ring organoid left of center, joined by two thin non-crossing pale-gray hairlines to (1) an upper-right inset showing magnified striated muscle texture and (2) a lower-right inset showing a magnified vessel cross-section with open lumen | PASS. Clean white background, no hard black outlines, no neon colors, no glow effects, no text, no heart, no scissors, no chart axes, no arrows. Both required zoom insets are present and correctly matched to their source detail (striation texture / vessel lumen), and the two hairlines connect cleanly without crossing. Open ring preserved, though the inner hole is a bit more tightly filled by the core coil than the single-subject variant — still reads as an open ring, not a filled disc. |

## Regeneration notes
- Both tasks generated cleanly on the first pass — zero HARD FAILs, zero regeneration retries needed.
- Run budget: 0 credits spent (guard-verified `cost=0` on every task before submission).
- Source files: `output/images/<task-id>_var1.webp` in the FireFly repo; these JPGs are 92%-quality re-encodes for review/commit into this repo.
- Prior rounds (`theme_candidates_v3/`, `theme_candidates_v4/`) remain in the repo for comparison; the corresponding v3 and v4 queue tasks are now disabled in favor of this v5 NEJM-style round.

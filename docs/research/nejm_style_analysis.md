# NEJM review-figure style: reverse-engineered block + candidate scoring

Date: 2026-08-29. Method: `journal-style-reverse-prompt` skill
(`~/.claude/skills/journal-style-reverse-prompt/SKILL.md`), created for this
task.

## Ground truth about NEJM figures (web-verified)

- NEJM publishes **no public style guide**. Every accepted figure is redrawn
  in-house by NEJM's Editorial Creative Media team (formerly Graphic Arts),
  staffed by professional medical illustrators using Illustrator/Photoshop
  (sources: NEJM Author Center; CSE interview with Kathy Stern, NEJM Graphic
  Arts Director; NEJM medical-illustrator job description).
- Figure tech specs: Arial/Helvetica 8–10 pt, must survive grayscale,
  1200 dpi line art. Review articles get up to 6 display items.
- NEJM policy forbids generative-AI content **inside submitted scientific
  images** — irrelevant for a lab website hero, but do not pitch these images
  as journal submissions.

## Reverse-engineered NEJM review-illustration STYLE BLOCK

Soft airbrushed gradient shading (Illustrator gradient-mesh feel); **no hard
dark outlines** — form modeled by tonal shifts and deeper edge tones; muted
naturalistic clinical palette (dusty rose, desaturated brick, slate blue, sage
green, warm tan, cream — nothing neon, nothing saturated); one soft diffuse
light from upper left, faint soft cast shadows; semi-3D didactic relief;
clean white background, generous margins; calm educational textbook tone.
Conventions: circular zoom insets joined by thin gray hairline leader lines;
Helvetica labels (composited in post — generation stays text-free).
NEVER: dark backgrounds, neon, chiaroscuro/rim light, film grain, glow,
hard black outlines, cartoon styling.

## Scoring the nine v3/v4 candidates against the block (0–2 per axis, 6 axes)

| # | Candidate | Rendering | Edges | Palette | Light | Background | Tone | Total /12 |
|---|---|---|---|---|---|---|---|---|
| 9 | light flat v4 (open ring) | 0 (flat) | 0 (hard outlines) | 2 | 1 | 2 | 2 | **7 — closest** |
| 4 | light flat v3 (filled disc) | 0 | 0 | 2 | 1 | 2 | 1 | 6 |
| 2 | dark illustration v3 | 2 (soft gradients) | 1 | 0 | 0 | 0 | 1 | 4 |
| 6 | cinematic v4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 |
| 1 | dark photo v3 | 1 | 1 | 0 | 0 | 0 | 0 | 2 |
| 8 | dark token field v4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 |
| 3 | token field split v3 | 1 | 0 | 0 | 0 | 1 | 0 | 2 |
| 5 | fluorescence micrograph v4 | 0 (photo) | 1 | 0 | 0 | 0 | 0 | 1 |
| 7 | eclipse v4 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |

Verdict: **candidate 9 is the most NEJM-like** but still misses the two
defining axes — NEJM models form with soft gradients and uses NO hard
outlines, while 9 is flat vector with dark outlines (a generic-infographic
look, not NEJM). True NEJM-style versions are generated as round v5
(`shen-theme-nejm-organoid-v5`, `shen-theme-nejm-scene-v5`), with reporter
colors muted into the clinical palette (green→sage, orange→terracotta tan,
cyan→slate blue).

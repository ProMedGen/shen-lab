# RQ8 — Image-model prompt engineering for a 2K 16:9 scientific hero

**Status: Partial.** Vendor rules for depth, narrative order, 2K/16:9, and
text handling are verified. No inspected vendor page publishes a template
with two filled text-free Nature/Science-cover scientific scenes. The
skeleton and two examples below are **constructed** from those rules plus
the verified biology in RQ1–RQ7. They are not copied from a source.

Google and OpenAI **disagree** on prompt order (subject-first narrative vs
background-first) and on negatives (positive framing vs explicit “no extra
text”). Adobe Firefly is front-weighted six layers. The skeleton below
puts the **focal subject first** (Firefly/Google weight) and still names
background, camera, and constraints (OpenAI).

## 1. Structures that produce layered depth

Verified:

- Split a complex scene into sequential steps: **background, then
  foreground, then focal object** (Gemini / Nano Banana best practices;
  misty-forest altar example).
- Name **camera, lens, and DOF**, including “low-angle shot with a shallow
  depth of field (f/1.8).”
- Photoreal template: shot type, subject, setting, light, camera angle,
  lens. 16:9 samples exist.

## 2. Vocabulary toward editorial scientific covers

Google formula: **[Subject] + [Action] + [Location/context] +
[Composition] + [Style]**. Not a keyword list.

Style anchors that are documented: magazine film grain, named lighting
(three-point softbox, chiaroscuro), material nouns (not “nice jacket”;
“navy blue tweed”).

OpenAI scientific samples are **labeled diagrams and charts**
(photosynthesis / cellular-respiration diagram; TAM/SAM/SOM slide). That
is the **infographic path**. A text-free hero must not use it.

Firefly: GPT Image 2 is marketed for **infographics with readable
in-image text** (up to six references). Gemini / Nano Banana is the better
seat for **complex multi-element scenes**. Use Gemini/Nano Banana for this
hero.

## 3. Multi-element scenes that stay distinct but integrated

- Sequential planes, one shared light, one named camera.
- Front-weight the focal subject (Firefly: most models weigh the front of
  the prompt more heavily).
- Nano Banana 2 “handles concise visual cues better than long paragraphs.”
- Native size: Gemini 3.1 Flash Image `aspect_ratio` 16:9, `image_size` 2K
  (also 1K/4K). gpt-image-2 recommended ceiling **2560×1440**; larger is
  experimental.

## 4. Failure modes and counters

Vendor-verified:

| Failure | Vendor counter |
| --- | --- |
| Garbled / extra type | Quote wanted copy and pre-generate it (Google), or “no extra text / no watermark” (OpenAI). Both still fail on misspellings, complex type, and placement. **Keep the hero type-free; add labels in post.** |
| Generic stock look | OpenAI: “Avoid clip art, stock photography… or anything that feels generic.” Google: editorial/photographic nouns, named materials. |
| Keyword salad | Google: narrative sentence, not a list. |

**Not named** on any inspected vendor page: “symmetric-icon syndrome,”
“love-heart prior,” “chart hallucination.” The counters below are
constructed from RQ1–RQ7 plus those vendor rules:

| Failure (lab-observed / requested) | Constructed counter |
| --- | --- |
| Love-heart prior | Never say “heart” as the subject. Say “cardiac crescent,” “beating bud,” “TNNT2 cardiomyocyte ring,” “vascularized cardiac organoid.” |
| Symmetric icon grid | Specify **asymmetric endothelial branching** and a doughnut, not six satellites. |
| Chart hallucination | Cover-style scene, not a diagram. No axes, bars, scatter, UMAP, or panel letters. Do not use Firefly’s GPT Image 2 infographic path. |
| Red+green cover clash | Green ring + **orange** plexus + cyan core. No SOX2-red. |
| Scissors / blue brain / tumor-vs-heart | Name bilobed protein, cell-on-circuit, or the three-beat care bar only if those objects are actually in the frame; otherwise omit. |

## 5. Template skeleton (constructed) + two filled 16:9 2K examples

Length budget: one to two short paragraphs plus a camera/constraint
block. Nano Banana prefers concise cues.

```
SUBJECT: <one living biological object, named with reporter geometry>
ACTION: <what it is doing: beating, branching, being selected>
SETTING: <dark 16:9 field; optional faint background plane>
MIDGROUND: <polarity or second plane, lower opacity>
MATERIALS / LIGHT: <named materials; one key + rim>
CAMERA: <angle, lens, f-stop, DOF>
STYLE: <editorial scientific-magazine photograph or named illustrator language>
CONSTRAINTS: text-free, no watermark, and the specific banned tropes for this frame
OUTPUT: 16:9, 2K (Gemini image_size=2K; gpt-image-2 at 2560x1440 if used)
```

### Example 1 — Blueprint 1 doughnut (primary hero)

Use on Gemini 3.1 / Nano Banana 2, native 16:9, 2K.

A living human vascularized cardiac organoid fills a dark navy 16:9 field.
Tightly packed flat iPSC-like cells with large nuclei form the outer
margin of a circular micropattern. They give way to a pulsatile green
TNNT2 cardiomyocyte ring. Orange CDH5 endothelial cells radiate outward
and branch through the myocardium as lumenized vessels four to forty
micrometres wide. Cyan-blue TAGLN smooth-muscle cells occupy the center
with a mural wrap. Behind the organoid, at lower opacity, an anterior
cTnT cardiac crescent condenses into a beating bud beside a gut-like
tube, split by a thin CD31 endocardial sheet; first-heart-field cells sit
more anterior than second-heart-field cells. A calcium wave and
millisecond displacement ticks mark contraction. A small near-edge patch
of cTnT cross-striations is visible in the sharp plane.

Low-angle editorial scientific-magazine photograph, 50 mm lens, shallow
depth of field f/1.8, chiaroscuro rim light on the orange vascular
plexus, pronounced film grain, empty dark navy void around the organoid.
No extra text, no watermark, no logos, no cartoon heart, no uniform
sphere, no glowing blob, no scissors, no red-and-green pairing, no
tumor, no neural net.

### Example 2 — Blueprint 2 virtual-cell reading

Use on Gemini 3.1 / Nano Banana 2, native 16:9, 2K. Not a substitute for
example 1.

A 16:9 scientific-magazine illustration, split dark and light. The left
half is a dark geometric lattice of oval cell tokens with square cores.
The right half is lighter: one biological cell seated on copper circuit
traces. A pointing hand selects one left-side token; that token expands
into a concentric vascularized organoid with a green cardiomyocyte ring,
orange endothelial branches, and a cyan smooth-muscle core, sharing the
same single light as the lattice.

Editorial geometric language in the lattice, photographic silicon-cell
language on the right, shared key light from upper left, shallow depth of
field on the expanded organoid, 50 mm, f/1.8. No extra text, no
watermark, no UMAP axes, no perceptron, no blue brain, no cartoon heart,
no scissors.

### Firefly routing

- **Hero, text-free, multi-element:** Gemini 3.1 / Nano Banana 2.
- **Later labeled infographic or in-image captions:** GPT Image 2, only
  after the hero exists; do not start there.
- Six Firefly layers, front-weighted: subject, setting, style,
  composition (DOF), lighting, model tags.

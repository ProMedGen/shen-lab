# Deep-research prompts for the research-themes hero figure

Feed each prompt separately to the Grok CLI. Save each answer as
`docs/research/grok/RQ<N>_<slug>.md` in this repo and tell the assistant —
it will read all of them and redesign the front-page schematic from the
findings. Every prompt asks for a structured markdown report with concrete,
drawable specifics (element inventories, composition geometry, color/light
specs), not general prose.

---

## RQ1 — Visual language of iPSC biology and cardiac differentiation

You are researching for a scientific illustrator designing a premium
website hero figure for a cardiovascular stem-cell lab. Topic: how induced
pluripotent stem cells (iPSCs) and directed cardiac differentiation are
depicted in the best figures of Cell, Nature, Science, Cell Stem Cell, and
in professional biomedical illustration (journal covers, BioRender showcase
work, NEJM illustrations).

Report, in markdown:
1. The canonical visual elements experts use for iPSC identity: colony
   morphology (tight round colonies with defined edges on feeder-free
   matrix), reprogramming arrows from somatic cells, pluripotency imagery.
   Describe each element's exact shapes, proportions, and typical colors.
2. How directed differentiation into cardiomyocytes, endothelial cells,
   pericytes, fibroblasts, smooth muscle, and epicardial cells is drawn:
   trajectory/waterfall layouts, Waddington landscapes, branching-tree
   metaphors. Which layouts read instantly and which need captions?
3. How beating cardiomyocytes and sarcomere striations are stylized when
   an illustration (not a micrograph) must "look alive": striation pattern,
   contraction motion cues, calcium-wave glow conventions.
4. Ten specific published figures or covers (cite journal/year/DOI or a
   findable description) that this figure should learn from, each with one
   sentence on what makes it vivid.
5. A DO/DON'T list for depicting stem cells without clichés.

## RQ2 — Visual language of developmental biology, organoids, and gastruloids

Same illustrator context. Topic: how human cardiac development,
vascularized organoids, and gastruloids are depicted vividly in top
journals (the lab's own Science 2025 gastruloid vascularization work is
the anchor; also cardiac organoid/"cardioid" papers in Cell/Nature).

Report:
1. Element inventory for embryonic heart development: heart-tube looping,
   chamber ballooning, epicardium, trabeculation — the exact shapes and
   stage sequence illustrators compress into 3-4 drawable stages.
2. How organoids and gastruloids are drawn to look three-dimensional and
   alive rather than like plain spheres: internal lumen hints, budding
   vasculature, translucency, cutaway conventions, nascent vessel networks
   (CD31-style branching) rendered as glowing traceries.
3. How "development as a process" is shown in a single static image:
   time-arrows, stage strips, spiral timelines, morphing sequences.
4. Ten reference figures/covers with one-line lessons.
5. DO/DON'T list.

## RQ3 — Visual language of CRISPR functional genomics and screens

Same illustrator context. Topic: how genome-scale CRISPR knockout/
interference/activation screens, variant knock-ins (VUS), and
druggable-genome screening are depicted in Cell/Nature/Science figures
and journal covers — beyond the cliché of "scissors cutting DNA".

Report:
1. Element inventory: Cas9/sgRNA complex shapes, guide libraries as
   barcoded pools, arrayed vs pooled screen layouts, multiwell plates with
   phenotype gradients, enrichment/depletion as visual flows (NOT as data
   charts — this figure must never contain axes or fake data).
2. How bidirectional screens (CRISPRi + CRISPRa) are shown as opposing
   forces: visual metaphors that worked in print (dials, dimmer switches,
   up/down particle flows).
3. How a "hit" emerging from thousands of perturbations is dramatized
   visually without a volcano plot.
4. Ten reference figures/covers with one-line lessons.
5. DO/DON'T list, including what makes CRISPR imagery look dated (2015-era
   scissor clipart) vs current.

## RQ4 — Visual language of multiomics and single-cell Perturb-seq

Same illustrator context. Topic: how single-cell multiomics (RNA-seq,
epigenomics, proteomics layers) and Perturb-seq are depicted vividly:
layered-data metaphors, cell-to-data transformations, UMAP-like clouds
(careful: must not look like a real data panel), barcoded droplets,
combinatorial perturbation grids.

Report:
1. Element inventory: omic layer stacks that look premium rather than
   like stacked rhombi — what texture/content hints (helix ribbon in the
   genome layer, peak tracks in the epigenome layer, molecule glyphs in
   the proteome layer) make layers read as OMICS specifically. Note the
   hard constraint: no readable letters or numbers anywhere.
2. Droplet microfluidics and cell-barcoding imagery: how cells flowing
   into droplets with barcode beads are stylized.
3. How "thousands of single cells each carrying a perturbation" is shown:
   particle fields, point-cloud galaxies with cluster coloring — and how
   to keep such a cloud clearly ILLUSTRATIVE (no axes, no legend) so it
   cannot be mistaken for data.
4. Ten reference figures/covers with one-line lessons.
5. DO/DON'T list.

## RQ5 — Visual language of machine learning and virtual-cell models in biology

Same illustrator context. Topic: how AI/ML in biology — foundation
models, virtual cells, in-silico perturbation prediction — is depicted
in current (2024-2026) journal art, avoiding both the dated "blue brain"
and the generic three-column perceptron.

Report:
1. Element inventory for a "virtual cell": digital-twin styling (wireframe
   or particle hologram of a cell/heart mirrored from the real one),
   latent-space imagery, transformer/attention motifs that read to
   scientists, prediction arrows looping back to experiments.
2. How the experiment→model→prediction→experiment loop (lab-in-the-loop)
   is drawn as a cycle; strongest circular-composition examples.
3. Current premium color/material language for AI in science illustration
   (glassmorphism, particle fields, gradient meshes) vs what looks like
   2018 stock art.
4. Ten reference figures/covers with one-line lessons.
5. DO/DON'T list.

## RQ6 — Visual language of cardio-oncology

Same illustrator context. Topic: how cardio-oncology — protecting the
heart during cancer therapy — is depicted: anthracycline/doxorubicin
cardiotoxicity, chemo damaging cardiomyocytes, cardioprotection,
survivorship. Journals: Circulation, JACC CardioOncology, Cancer Cell,
plus pharma/medical illustration.

Report:
1. Element inventory: how "drug that fights the tumor but threatens the
   heart" is drawn as one visual — dual-action arrows, shielded heart
   receiving chemo, damaged vs protected myocardium side by side, tumor
   cell + cardiomyocyte contrast.
2. How toxicity is stylized (fraying sarcomeres, mitochondrial damage,
   dark lesions) without being gruesome on a lab homepage.
3. How protection/rescue is stylized (shield conventions, small-molecule
   binding, glow restoration) without looking like a pharma ad.
4. Ten reference figures/covers with one-line lessons.
5. DO/DON'T list.

## RQ7 — Integration: composing six themes into one narrative masterpiece

The synthesis prompt — most important. Context: a cardiovascular
precision-medicine lab needs ONE integrated hero figure containing six
themes (iPSC, developmental biology, functional genomics, multiomics,
machine learning, cardio-oncology). The lab's real pipeline: patient/
healthy iPSCs → differentiation into all cardiovascular cell types and
vascularized organoids (developmental biology insight) → CRISPR screens
and variant knock-ins (functional genomics) → single-cell multiomic and
Perturb-seq readouts (multiomics) → training virtual-cell foundation
models (machine learning) → nominated targets and cardioprotective
therapies, especially protecting cancer survivors' hearts
(cardio-oncology) → back to patient cells. Research how master
integrative figures are composed:

1. Composition archetypes for 5-7 concept integration: radial hub-and-
   spoke, circular cycle (virtuous loop), left-to-right pipeline,
   landscape/scene metaphor (city, river, orbit system), central-organ
   anatomy with themed "districts". For each: when it wins, when it
   fails, 2-3 published examples (graphical abstracts, review-article
   summary figures, journal covers).
2. Narrative flow: how the best figures give a READING ORDER (entry
   point, path, payoff) rather than six equal satellites. How arrows,
   scale progression, and light direction create that order.
3. Depth and vividness mechanics specifically: layering foreground/
   midground/background, atmospheric perspective in illustration,
   focal glow hierarchy, overlapping elements vs isolated icons,
   texture density gradients. Why "six icons around a hub" reads flat
   and what concretely fixes it.
4. Color systems for six-theme figures: assigning each theme a hue while
   keeping one dominant brand tone (deep navy + red accent in this case);
   examples of six-hue systems that stayed harmonious.
5. Three concrete composition blueprints (described in enough geometric
   detail to draw: what is at center, what flows where, relative sizes,
   light sources), ranked by fit for a dark premium lab-website hero at
   16:9 that must also survive at 400px width on mobile.

## RQ8 — Image-model prompt engineering for journal-grade scientific scenes (2026)

Context: the figure is generated with image models (Gemini 3.1 / Nano
Banana 2, GPT Image 2 via Adobe Firefly), text-free (typography is
composited afterward). Research current best practice for prompting
image models to produce integrated scientific scenes with depth:

1. Prompt structures that reliably produce layered depth (foreground/
   midground/background separation, atmospheric haze, focal depth of
   field) rather than flat icon layouts.
2. Vocabulary that steers toward premium scientific-editorial
   illustration (the Nature/Science cover look) and away from emoji/
   clipart/stock-vector defaults; concrete style-anchor phrases that
   work in 2025-2026 models.
3. How to specify multi-element scenes so elements stay DISTINCT but
   INTEGRATED (shared perspective, shared light) instead of merging or
   fragmenting into a grid; ordering and weighting tricks.
4. Known failure modes for schematic scenes (symmetric icon syndrome,
   love-heart prior for "heart", garbled pseudo-text, chart
   hallucination) and the prompt-level counters for each.
5. A template prompt skeleton (sections, ordering, length budget) for a
   2K 16:9 integrated scientific hero scene, with two filled examples.

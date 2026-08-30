# RQ4 — Visual language of multiomics and single-cell Perturb-seq

**Status: Thin / Partial.** This is the weakest RQ in the packet. One
candidate claim was **rejected** at verification. Premium omic-layer
stacks with helix / peak-track / protein glyphs and no readable type were
**not found** as documented cover or schematic art in the pages inspected.

## 1. Omic layer stacks

**Not found.** No inspected Cell / Nature / Science cover or schematic in
this pass shows a type-free, premium RNA / epigenome / proteome stack
with helix ribbon, peak tracks, and molecule glyphs.

Do not invent that stack as a journal convention. If a multiomic reading
is needed, use RQ5/RQ7 blueprint 2 (oval cell tokens + silicon cell)
rather than stacked rhombi.

## 2. Droplet microfluidics and barcoding

**Rejected claim:** “Droplet single-cell illustrations show one cell with
a barcoded bead and three index layers: cell barcode, UMI, and a
guide/perturbation barcode.”

What actually holds:

- **Drop-seq** (Macosko): one cell co-encapsulated with a barcoded bead in
  a nanoliter droplet. Layers are PCR handle, **cell barcode, UMI,
  oligo-dT**. No guide barcode.
- **Perturb-seq / 10x capture** (Dixit, Adamson, Replogle): add a
  **guide/perturbation barcode** (GBC or captured sgRNA) on top of CBC +
  UMI.

Do **not** draw a three-index droplet as the default single-cell glyph.
If Perturb-seq is the subject, the extra GBC is allowed and should be
labeled only in post, not as in-image type.

## 3. Thousands of perturbed cells

When Perturb-seq papers dramatize thousands of perturbations:

- **Labeled embedding / UMAP-style point clouds and heatmaps are data
  figures** (Replogle Fig. 2D minimum-distortion embedding with cluster
  function labels; genotype-phenotype heatmaps).
- Graphical abstracts are **unlabeled workflow cartoons**.
- A galaxy of dots **with axes or letters** will be read as a data panel.
  For a type-free hero, do not use a UMAP.

No inspected Cell / Nature / Science **cover** used an unlabeled
illustrative cell-cloud galaxy in this pass. The inspected Science CRISPR
cover is a tomato-seedling **photograph**.

## 4. Inspected figures (partial catalog)

| Source | One-line lesson |
| --- | --- |
| Macosko et al., Drop-seq | Cell + bead in a droplet; CBC/UMI/oligo-dT, not a guide barcode. |
| Dixit et al., Perturb-seq | GBC is an extra, screen-specific index; graphical abstract is a workflow cartoon. |
| Replogle et al., 2022 | Embeddings and heatmaps = data; keep them out of the hero. |
| Science 365(6452) cover | CRISPR in culture can be a photograph, not a point cloud. |

## 5. DO / DON’T

**DO**

- Keep Perturb-seq as an unlabeled workflow (library → cell → readout).
- If a field of cells is needed, use Nature’s **oval tokens with square
  cores** (RQ5), which already reads as “many cells” without axes.
- Add GBC only when the story is Perturb-seq, not generic scRNA.

**DON’T**

- Stacked rhombi as “multiomics.”
- UMAP / t-SNE with axes, legends, or cluster letters in the hero.
- Three-layer droplet (CBC+UMI+GBC) as the default for all single-cell art.
- Readable gene names, barcodes, or panel letters in a type-free frame.

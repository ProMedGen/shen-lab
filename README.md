# Shen Lab · Cardiovascular Precision Medicine

Private, members-only website for the Cardiovascular Precision Medicine Lab (Shen Lab) at Washington University School of Medicine.

- Repository: https://github.com/ProMedGen/shen-lab
- Site (org members, after GitHub login): https://super-adventure-gwynznl.pages.github.io/
- Pages settings: https://github.com/ProMedGen/shen-lab/settings/pages

Led by **Mengcheng Shen, PhD**, Assistant Professor of Medicine and of Developmental Biology.

## Publish

The site is static HTML. GitHub Actions deploys it to GitHub Pages.

1. Repository visibility: **private**
2. Settings → Pages → Source: **GitHub Actions**
3. Settings → Pages → Visibility: **Private** (members with read access)

Private Pages are served on a unique `*.pages.github.io` subdomain, not on `promedgen.github.io/shen-lab`.

## Local preview

```bash
python3 -m http.server 4173
```

Then open `http://127.0.0.1:4173`.

## Source materials

Lab photographs, movies, and the research-focus document live locally in `Shen Lab WashU_lab_website_materials/` and are not committed. Web-sized copies are in `assets/`.

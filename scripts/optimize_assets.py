#!/usr/bin/env python3
"""Convert Shen Lab source materials into web-sized images and videos."""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

SRC = Path("/Volumes/CrucialX10A/Apps/Website/Shen_Lab/Shen Lab WashU_lab_website_materials")
IMG = Path("/Volumes/CrucialX10A/Apps/Website/Shen_Lab/assets/img")
VID = Path("/Volumes/CrucialX10A/Apps/Website/Shen_Lab/assets/video")
IMG.mkdir(parents=True, exist_ok=True)
VID.mkdir(parents=True, exist_ok=True)


def white_to_alpha(im: Image.Image, floor: float = 0.035) -> Image.Image:
    """Treat white paper as transparent and recover anti-aliased ink color."""
    arr = np.asarray(im.convert("RGBA"), dtype=np.float32)
    rgb = arr[..., :3]
    alpha = ((255.0 - rgb) / 255.0).max(axis=2)
    alpha = np.where(alpha < floor, 0.0, np.clip(alpha, 0.0, 1.0))
    fg = (rgb - 255.0) / np.maximum(alpha[..., None], 1e-6) + 255.0
    out = np.empty_like(arr)
    out[..., :3] = np.clip(fg, 0, 255)
    out[..., 3] = alpha * 255.0
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def trim_whitespace(im: Image.Image, threshold: int = 245) -> Image.Image:
    gray = ImageOps.grayscale(im.convert("RGB"))
    bw = gray.point(lambda p: 255 if p < threshold else 0)
    bbox = bw.getbbox()
    if not bbox:
        return im
    pad = 12
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(im.width, bbox[2] + pad)
    bottom = min(im.height, bbox[3] + pad)
    return im.crop((left, top, right, bottom))


def save_jpeg(im: Image.Image, dest: Path, max_w: int = 1800, quality: int = 82) -> None:
    rgb = im.convert("RGB")
    if rgb.width > max_w:
        ratio = max_w / rgb.width
        rgb = rgb.resize((max_w, int(rgb.height * ratio)), Image.Resampling.LANCZOS)
    rgb.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)


def save_png(im: Image.Image, dest: Path, max_w: int = 1200) -> None:
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")
    if im.width > max_w:
        ratio = max_w / im.width
        im = im.resize((max_w, int(im.height * ratio)), Image.Resampling.LANCZOS)
    im.save(dest, "PNG", optimize=True)


def convert_image(name: str, dest_name: str, kind: str = "photo", max_w: int = 1800) -> None:
    src = SRC / name
    dest = IMG / dest_name
    im = Image.open(src)
    if kind == "logo":
        im = white_to_alpha(im)
        alpha = im.getchannel("A")
        bbox = alpha.point(lambda p: 255 if p > 10 else 0).getbbox()
        if bbox:
            pad = 16
            im = im.crop((
                max(0, bbox[0] - pad),
                max(0, bbox[1] - pad),
                min(im.width, bbox[2] + pad),
                min(im.height, bbox[3] + pad),
            ))
        save_png(im, dest, max_w=max_w)
    elif kind == "logo-banner":
        im = trim_whitespace(im, threshold=8)
        save_png(im.convert("RGBA"), dest, max_w=max_w)
    else:
        save_jpeg(im, dest, max_w=max_w, quality=82)
    print(f"img {dest.name:40s} {dest.stat().st_size / 1024:8.1f} KB")


def ffmpeg(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def encode_video(
    src_name: str,
    dest_name: str,
    start: float | None = None,
    duration: float | None = None,
    max_w: int = 1280,
) -> None:
    dest = VID / dest_name
    cmd = ["ffmpeg", "-y"]
    if start is not None:
        cmd += ["-ss", str(start)]
    cmd += ["-i", str(SRC / src_name)]
    if duration is not None:
        cmd += ["-t", str(duration)]
    cmd += [
        "-vf", f"scale='min({max_w},iw)':-2",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "28",
        "-preset", "slow",
        "-an",
        "-movflags", "+faststart",
        str(dest),
    ]
    ffmpeg(cmd)
    print(f"vid {dest.name:40s} {dest.stat().st_size / 1024:8.1f} KB")


def still_from_video(src_name: str, dest_name: str, at: float = 2.0) -> None:
    dest = IMG / dest_name
    ffmpeg([
        "ffmpeg", "-y", "-ss", str(at), "-i", str(SRC / src_name),
        "-frames:v", "1", "-q:v", "3", str(dest),
    ])
    im = Image.open(dest)
    save_jpeg(im, dest, max_w=1600, quality=80)
    print(f"still {dest.name:38s} {dest.stat().st_size / 1024:8.1f} KB")


def main() -> None:
    convert_image("Shen Lab Logo_Small.tiff", "logo.png", kind="logo", max_w=900)
    # WashU Medicine lockup: use official SVG from medicine.washu.edu, not the folder raster.
    convert_image("Center For Cardiovascular Research.png", "cvr-center.png", kind="logo", max_w=560)
    convert_image("Headshot_Mengcheng Shen.png", "headshot.jpg", max_w=900)
    convert_image("Lab research focus.png", "research-overview.jpg", max_w=2000)
    convert_image("Cardio-oncology.jpg", "cardio-oncology.jpg", max_w=1400)
    convert_image(
        "CRISPR screen pipeline in precison cardio-oncology medicine.png",
        "crispr-pipeline.jpg",
        max_w=2000,
    )
    convert_image(
        "High-efficiency iPSC-endothelial cell differentiation.png",
        "endothelial-protocol.jpg",
        max_w=2000,
    )
    convert_image("iPSC-cardiomyocytes_Cardiac troponin T_red.png", "cm-ctnt.jpg", max_w=1600)
    convert_image("iPSC-epicardial cells_ZO-1_red, WT1_Cyan.png", "epicardial.jpg", max_w=1400)
    convert_image("iPSC-cardiac pericytes,αSMA_green, PDGFRβ_red.png", "pericytes.jpg", max_w=1400)
    convert_image("iPSC-cardiac fibroblasts, TE-7_red.png", "fibroblasts.jpg", max_w=1400)
    convert_image("iPSC-cardiac smooth muscle cells, MYH11_red.jpg", "smc-myh11.jpg", max_w=1400)
    convert_image("iPSC-vessel organoids.png", "vessel-organoid.jpg", max_w=1400)

    # The specimen clips on the Models page autoplay on a loop, so they are cut
    # to a few representative seconds and capped at 960px. Left at full length
    # (17s and 30s) these two alone were 7.5 MB of the page.
    encode_video("iPSC-cardiomyocytes, beating1.mov", "cm-beating.mp4",
                 start=2.0, duration=6.0, max_w=960)
    encode_video("iPSC-cardiomyocytes, beating_MYL7 in green.mov", "cm-myl7.mp4")
    encode_video("iPSC-engineered heart tissues_brightfield.mp4", "eht-brightfield.mp4")
    encode_video("iPSC-engineered heart tissues_MYL7_eGFP.mp4", "eht-myl7.mp4")
    encode_video("iPSC-cardiac orgaoids.mov", "cardiac-organoids.mp4")
    encode_video("iPSC-vascularized cardiac organoids.mp4", "vascularized-organoids.mp4",
                 start=6.0, duration=7.0, max_w=960)
    encode_video(
        "iPSC-vessel organoids,CD31 (endothelial cells, magenta), PDGFR-β (mural cells, yellow) and Collagen IV (basement membrane, cyan).mp4",
        "vessel-organoids.mp4",
    )
    encode_video("Lab space.MOV", "lab-space.mp4", start=2.0, duration=7.0)
    encode_video("Tissue culture room.MOV", "tissue-culture.mp4", start=2.0, duration=7.0)

    still_from_video("Lab space.MOV", "lab-space.jpg", at=3.5)
    still_from_video("Tissue culture room.MOV", "tissue-culture.jpg", at=3.5)
    still_from_video("iPSC-cardiomyocytes, beating1.mov", "cm-beating-poster.jpg", at=1.0)
    still_from_video("iPSC-cardiac orgaoids.mov", "cardiac-organoid-poster.jpg", at=1.5)

    total = sum(p.stat().st_size for p in list(IMG.glob("*")) + list(VID.glob("*")))
    print(f"TOTAL {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()

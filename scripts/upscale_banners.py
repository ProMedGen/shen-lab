#!/usr/bin/env python3
"""Faithfully upscale banner sources and write 16:9 cover crops.

Uses Real-ESRGAN (ncnn) when available; otherwise ffmpeg Lanczos.
Never generative — biology pixels stay the same structure.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
OUT = IMG / "banners"
REALESRGAN = Path("/tmp/esrgan-full/realesrgan-ncnn-vulkan")
REALESRGAN_MODELS = Path("/tmp/esrgan-full/models")

# source relative to assets/img → banner stem
JOBS = {
    "cm-ctnt.jpg": "home",
    "fibroblasts.jpg": "research",  # unique stain; avoid annotated overview diagrams
    "vessel-organoid.jpg": "models",
    "pericytes.jpg": "pubs",
    "smc-myh11.jpg": "contact",
    "epicardial.jpg": "404",
    "tissue-culture.jpg": "join",
    "lab-space.jpg": "lab-space-up",
}

TARGET_LONG = 2560  # ≥2K class on long edge before crop
BANNER_W, BANNER_H = 2560, 1440  # 16:9 cover


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def upscale(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    w, h = Image.open(src).size
    long_edge = max(w, h)
    if long_edge >= TARGET_LONG and dest.suffix.lower() in {".jpg", ".jpeg"}:
        # already large enough — just copy then crop path handles resize
        shutil.copy2(src, dest)
        print(f"copy {src.name} ({w}x{h}) — already ≥{TARGET_LONG}")
        return

    scale = 4 if long_edge < 1280 else 2
    if REALESRGAN.exists():
        # realesrgan writes png; convert after
        tmp = dest.with_suffix(".png")
        run(
            [
                str(REALESRGAN),
                "-i",
                str(src),
                "-o",
                str(tmp),
                "-m",
                str(REALESRGAN_MODELS),
                "-n",
                "realesrgan-x4plus",
                "-s",
                str(scale),
                "-f",
                "png",
            ]
        )
        im = Image.open(tmp).convert("RGB")
        im.save(dest, "JPEG", quality=90, optimize=True)
        tmp.unlink(missing_ok=True)
    else:
        # ffmpeg lanczos to target long edge
        if w >= h:
            vf = f"scale={TARGET_LONG}:-1:flags=lanczos"
        else:
            vf = f"scale=-1:{TARGET_LONG}:flags=lanczos"
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(src),
                "-vf",
                vf,
                "-q:v",
                "2",
                str(dest),
            ]
        )
    ow, oh = Image.open(dest).size
    print(f"upscaled {src.name} → {dest.name} ({ow}x{oh})")


def cover_crop(src: Path, dest: Path, tw: int = BANNER_W, th: int = BANNER_H) -> None:
    im = Image.open(src).convert("RGB")
    # scale to cover
    scale = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=88, optimize=True)
    print(f"banner {dest.name} {tw}x{th} from {src.name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, stem in JOBS.items():
        src = IMG / src_name
        if not src.exists():
            print(f"MISSING {src}", file=sys.stderr)
            continue
        up = OUT / f"{stem}-up.jpg"
        banner = OUT / f"banner-{stem}.jpg"
        upscale(src, up)
        # home/research/models/pubs/contact/404/join get banner-* names
        if stem.endswith("-up"):
            continue
        cover_crop(up, OUT / f"banner-{stem}.jpg")
    print("done →", OUT)


if __name__ == "__main__":
    main()

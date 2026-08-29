#!/usr/bin/env python3
"""Extract a poster frame for every clip in assets/video.

Posters let the Models page ship with `preload="none"` on each <video>: the
browser paints the poster and downloads nothing until the visitor presses play.
Frames come from the committed mp4s, so this runs without the private source
materials in `Shen Lab WashU_lab_website_materials/`.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
VID = ROOT / "assets" / "video"
IMG = ROOT / "assets" / "img"

# Seek time per clip, chosen so the frame is representative rather than a
# fade-in or an empty field of view.
FRAME_AT = {
    "cm-beating.mp4": 1.0,
    "cm-myl7.mp4": 1.0,
    "eht-brightfield.mp4": 2.0,
    "eht-myl7.mp4": 1.5,
    "cardiac-organoids.mp4": 1.5,
    "vascularized-organoids.mp4": 6.0,
    "vessel-organoids.mp4": 4.0,
    "lab-space.mp4": 3.0,
    "tissue-culture.mp4": 3.0,
}

# Clips whose poster already exists under a curated name from optimize_assets.py.
EXISTING = {
    "cm-beating.mp4": "cm-beating-poster.jpg",
    "cardiac-organoids.mp4": "cardiac-organoid-poster.jpg",
    "lab-space.mp4": "lab-space.jpg",
    "tissue-culture.mp4": "tissue-culture.jpg",
}


def poster_name(clip: str) -> str:
    return EXISTING.get(clip, f"{Path(clip).stem}-poster.jpg")


def extract(clip: Path, dest: Path, at: float) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(at), "-i", str(clip),
         "-frames:v", "1", "-q:v", "2", str(dest)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    with Image.open(dest) as im:
        im.convert("RGB").save(dest, "JPEG", quality=78, optimize=True, progressive=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force", action="store_true",
        help="Re-extract posters that already exist. Needed after re-encoding a "
             "clip, since a kept poster would still show the old footage.",
    )
    args = parser.parse_args()

    for clip_name, at in FRAME_AT.items():
        clip = VID / clip_name
        if not clip.exists():
            print(f"skip {clip_name} (missing)")
            continue
        dest = IMG / poster_name(clip_name)
        if dest.exists() and clip_name in EXISTING and not args.force:
            print(f"keep {dest.name:32s} {dest.stat().st_size / 1024:7.1f} KB")
            continue
        extract(clip, dest, at)
        with Image.open(dest) as im:
            dims = f"{im.width}x{im.height}"
        print(f"made {dest.name:32s} {dest.stat().st_size / 1024:7.1f} KB  {dims}")


if __name__ == "__main__":
    main()

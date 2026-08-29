#!/usr/bin/env python3
"""Faithfully upscale low-res content figures and video posters, IN PLACE.

Same filenames are kept so all existing HTML/CSS references keep working;
run scripts/build_pages.py afterward to refresh the embedded width/height
attributes. Never generative — biology pixels stay the same structure.

Pipeline per file:
  1. Real-ESRGAN x4plus at -s 4 (its only native scale; -s 2 scrambles
     tiles on this ncnn build).
  2. Faithfulness gate vs. the original (downscale-back correlation/MAD).
  3. Lanczos downscale to a per-category long-edge cap (never upscaled
     beyond the 4x result — if 4x is already smaller than the cap, keep
     the 4x size).
  4. Save as JPEG quality 85 (optimize), replacing the original in place.

A copy of every original is stashed in /tmp/figure-originals/ first, as a
safety net beyond git history.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
ORIGINALS_BACKUP = Path("/tmp/figure-originals")

REALESRGAN = Path("/tmp/esrgan-full/realesrgan-ncnn-vulkan")
REALESRGAN_MODELS = Path("/tmp/esrgan-full/models")

# Real-ESRGAN's x4plus model natively produces 4x output only. Passing -s 2
# to the ncnn binary with this model corrupts the internal tile reassembly
# and produces a jumbled mosaic, not a smaller-but-correct upscale. Always
# request -s 4 and let the Lanczos downscale step do any subsequent resize.
REALESRGAN_SCALE = 4

MIN_CORRELATION = 0.9
MAX_MAD = 25.0  # on a 0-255 grayscale scale

SKIP_LONG_EDGE = 1600  # skip files already at/above this on the long edge

FIGURE_CAP = 2000  # long-edge cap for content figures
POSTER_CAP = 1440  # long-edge cap for *-poster.jpg video posters

JPEG_QUALITY = 85

TARGETS = [
    "epicardial.jpg",
    "fibroblasts.jpg",
    "smc-myh11.jpg",
    "headshot.jpg",
    "pericytes.jpg",
    "cm-ctnt.jpg",
    "cm-myl7-poster.jpg",
    "eht-myl7-poster.jpg",
    "eht-brightfield-poster.jpg",
    "vascularized-organoids-poster.jpg",
    "cm-beating-poster.jpg",
    "cardiac-organoid-poster.jpg",
    "vessel-organoids-poster.jpg",
    "lab-space.jpg",
    "tissue-culture.jpg",
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def faithfulness_check(original: Path, upscaled: Path) -> tuple[float, float, bool]:
    """Detect tiling/mosaic corruption by comparing upscaled output to source.

    Downscales the upscaled image back to the source's exact dimensions with
    Lanczos, converts both to grayscale, and compares them. Uses Pearson
    correlation via numpy when available; otherwise falls back to a
    pure-PIL mean-absolute-difference (MAD) proxy so the check has no hard
    numpy dependency. Returns (correlation, mad, passed).
    """
    src_im = Image.open(original).convert("L")
    up_im = Image.open(upscaled).convert("L")
    check_im = up_im.resize(src_im.size, Image.Resampling.LANCZOS)

    try:
        import numpy as np

        a = np.asarray(src_im, dtype=np.float64).ravel()
        b = np.asarray(check_im, dtype=np.float64).ravel()
        a_c, b_c = a - a.mean(), b - b.mean()
        denom = float(np.sqrt((a_c**2).sum()) * np.sqrt((b_c**2).sum()))
        corr = float((a_c * b_c).sum() / denom) if denom else 0.0
        mad = float(np.abs(a - b).mean())
    except ImportError:
        diff = ImageChops.difference(src_im, check_im)
        mad = ImageStat.Stat(diff).mean[0]
        # No numpy → approximate correlation from normalized MAD. This is a
        # monotonic stand-in, not true Pearson r, but is sufficient to catch
        # the gross pixel-shuffling a mosaic artifact produces.
        corr = 1.0 - (mad / 255.0)

    passed = corr >= MIN_CORRELATION and mad <= MAX_MAD
    return corr, mad, passed


def realesrgan_upscale(src: Path, tmp_png: Path) -> None:
    run(
        [
            str(REALESRGAN),
            "-i",
            str(src),
            "-o",
            str(tmp_png),
            "-m",
            str(REALESRGAN_MODELS),
            "-n",
            "realesrgan-x4plus",
            "-s",
            str(REALESRGAN_SCALE),
            "-f",
            "png",
        ]
    )


def lanczos_cap(im: Image.Image, cap: int) -> Image.Image:
    """Downscale (never upscale) so the long edge == cap, preserving aspect."""
    w, h = im.size
    long_edge = max(w, h)
    if long_edge <= cap:
        return im
    scale = cap / long_edge
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def process(name: str) -> tuple[bool, str]:
    src = IMG / name
    if not src.exists():
        return False, f"MISSING {src}"

    orig_w, orig_h = Image.open(src).size
    orig_kb = src.stat().st_size / 1024
    long_edge = max(orig_w, orig_h)

    if long_edge >= SKIP_LONG_EDGE:
        msg = (
            f"SKIP {name}: long edge {long_edge} already >= {SKIP_LONG_EDGE} "
            f"({orig_w}x{orig_h}, {orig_kb:.1f}KB)"
        )
        print(msg)
        return True, msg

    ORIGINALS_BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, ORIGINALS_BACKUP / name)

    tmp_png = src.with_name(f".{src.stem}-4x.png")
    realesrgan_upscale(src, tmp_png)

    corr, mad, passed = faithfulness_check(src, tmp_png)
    status = "PASS" if passed else "FAILED"
    up_w, up_h = Image.open(tmp_png).size
    print(
        f"{status} faithfulness {name}: corr={corr:.4f} mad={mad:.2f} "
        f"(4x output {up_w}x{up_h})"
    )
    if not passed:
        tmp_png.unlink(missing_ok=True)
        return False, f"FAILED {name}: corr={corr:.4f} mad={mad:.2f}"

    cap = POSTER_CAP if name.endswith("-poster.jpg") else FIGURE_CAP
    im = Image.open(tmp_png).convert("RGB")
    im = lanczos_cap(im, cap)
    final_w, final_h = im.size

    quality = JPEG_QUALITY
    im.save(src, "JPEG", quality=quality, optimize=True)
    tmp_png.unlink(missing_ok=True)

    new_kb = src.stat().st_size / 1024
    if new_kb > 1500:
        quality = 82
        im.save(src, "JPEG", quality=quality, optimize=True)
        new_kb = src.stat().st_size / 1024
        print(f"  re-saved {name} at quality={quality} to stay under ~1.5MB")

    print(
        f"{name}: {orig_w}x{orig_h} ({orig_kb:.1f}KB) -> "
        f"{final_w}x{final_h} ({new_kb:.1f}KB) q={quality}"
    )
    return True, (
        f"{status} {name}: corr={corr:.4f} mad={mad:.2f} "
        f"{orig_w}x{orig_h}->{final_w}x{final_h} {orig_kb:.1f}KB->{new_kb:.1f}KB"
    )


def main() -> int:
    if not REALESRGAN.exists() or not REALESRGAN_MODELS.exists():
        print(
            f"ERROR: Real-ESRGAN binary/models not found at {REALESRGAN} — "
            "this script requires it (no ffmpeg fallback).",
            file=sys.stderr,
        )
        return 1

    any_failed = False
    summary: list[str] = []
    for name in TARGETS:
        ok, msg = process(name)
        summary.append(msg)
        if not ok:
            any_failed = True

    print("\n--- summary ---")
    for line in summary:
        print(line)

    if any_failed:
        print(
            "\nFAILED: one or more upscaled figures failed the faithfulness "
            "check (likely tiling/mosaic corruption) — not safe to ship.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

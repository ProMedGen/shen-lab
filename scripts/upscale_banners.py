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

from PIL import Image, ImageChops, ImageStat

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

# Real-ESRGAN's x4plus model natively produces 4x output only. Passing -s 2
# to the ncnn binary with this model corrupts the internal tile reassembly
# and produces a jumbled mosaic, not a smaller-but-correct upscale. Always
# request -s 4 and let cover_crop() do any subsequent Lanczos downsizing.
REALESRGAN_SCALE = 4

MIN_CORRELATION = 0.9
MAX_MAD = 25.0  # on a 0-255 grayscale scale (i.e. 25/255 normalized)


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


def upscale(src: Path, dest: Path) -> tuple[float, float, bool]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    w, h = Image.open(src).size
    long_edge = max(w, h)
    if long_edge >= TARGET_LONG and dest.suffix.lower() in {".jpg", ".jpeg"}:
        # already large enough — just copy then crop path handles resize
        shutil.copy2(src, dest)
        print(f"copy {src.name} ({w}x{h}) — already ≥{TARGET_LONG}")
        return faithfulness_check(src, dest)

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
                str(REALESRGAN_SCALE),
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
    return faithfulness_check(src, dest)


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
    if not REALESRGAN.exists() or not REALESRGAN_MODELS.exists():
        print(
            f"NOTE: Real-ESRGAN binary/models not found at {REALESRGAN} — "
            "falling back to ffmpeg Lanczos upscaling.",
            file=sys.stderr,
        )
    any_failed = False
    for src_name, stem in JOBS.items():
        src = IMG / src_name
        if not src.exists():
            print(f"MISSING {src}", file=sys.stderr)
            continue
        up = OUT / f"{stem}-up.jpg"
        banner = OUT / f"banner-{stem}.jpg"
        corr, mad, passed = upscale(src, up)
        status = "PASS" if passed else "FAILED"
        print(f"{status} faithfulness {up.name}: corr={corr:.4f} mad={mad:.2f}")
        if not passed:
            any_failed = True
        # home/research/models/pubs/contact/404/join get banner-* names
        if stem.endswith("-up"):
            continue
        cover_crop(up, OUT / f"banner-{stem}.jpg")
    print("done →", OUT)
    if any_failed:
        print(
            "FAILED: one or more upscaled banners failed the faithfulness "
            "check (likely tiling/mosaic corruption) — not safe to ship.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

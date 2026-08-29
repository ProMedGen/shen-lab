#!/usr/bin/env python3
"""Check the built site in a real browser.

Start a server first:

    python3 -m http.server 4173
    .venv/bin/python scripts/verify_site.py

Beyond smoke-testing every page, this locks in three regressions that are easy
to reintroduce and invisible in review:

* lazy-loaded images must actually resolve once scrolled into view;
* in-page anchors must not land underneath the sticky header;
* page transfer size must stay inside budget (Models shipped 12 MB before every
  clip got preload="none" and a poster).
"""

from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "scripts" / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)
BASE = "http://127.0.0.1:4173"
PAGES = [
    "index.html",
    "research.html",
    "models.html",
    "publications.html",
    "news.html",
    "people.html",
    "join.html",
    "contact.html",
    "404.html",
]
MISSION = "The Cardiovascular Precision Medicine Lab is led by Dr. Mengcheng Shen"

# Transfer-size ceilings in KB, roughly 1.5x current size so ordinary content
# edits pass but a re-added eager video or an unoptimised figure does not.
WEIGHT_BUDGET_KB = {
    "index.html": 2000,
    "research.html": 2200,
    "models.html": 3400,
    "publications.html": 1400,
    "news.html": 700,
    "people.html": 800,
    "join.html": 700,
    "contact.html": 1500,
    "404.html": 700,
}

# Anchors reached from elsewhere in the site. Each must clear the sticky header.
ANCHORS = [
    ("research.html", "differentiation"),
    ("research.html", "genomics"),
    ("research.html", "modeling"),
    ("research.html", "cardio-oncology"),
    ("research.html", "perturb-seq"),
    ("publications.html", "y2026"),
    ("publications.html", "y2019"),
    ("publications.html", "y2014"),
]

SETTLE = """async () => {
    const step = window.innerHeight * 0.8;
    for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 120));
    }
    window.scrollTo(0, 0);
}"""

# Third-party metric badges are outside our control and flake in headless runs,
# so only images served by this site are treated as must-load.
LOCAL_IMAGES_LOADED = """() => [...document.images]
    .filter(i => new URL(i.currentSrc || i.src, location.href).origin === location.origin)
    .every(i => i.complete)"""

BROKEN_LOCAL_IMAGES = """() => [...document.images]
    .filter(i => new URL(i.currentSrc || i.src, location.href).origin === location.origin)
    .filter(i => i.naturalWidth === 0)
    .map(i => i.currentSrc || i.src)"""

HEADER_OVERLAP = """(id) => {
    const target = document.getElementById(id);
    if (!target) return null;
    const header = document.querySelector('.site-header');
    return Math.round(header.getBoundingClientRect().bottom
                      - target.getBoundingClientRect().top);
}"""


def check_page(page, path: str, problems: list[str]) -> None:
    transferred = [0]

    def on_response(response):
        if urlparse(response.url).hostname not in ("127.0.0.1", "localhost"):
            return
        try:
            transferred[0] += int(response.headers.get("content-length") or 0)
        except ValueError:
            pass

    page.on("response", on_response)
    page.goto(f"{BASE}/{path}", wait_until="load", timeout=30000)
    page.evaluate(SETTLE)
    try:
        page.wait_for_function(LOCAL_IMAGES_LOADED, timeout=30000)
    except Exception:
        problems.append(f"{path}: images never finished loading")
    page.wait_for_timeout(400)
    page.remove_listener("response", on_response)

    broken = page.evaluate(BROKEN_LOCAL_IMAGES)
    if broken:
        problems.append(f"{path}: broken images {broken}")

    if "Shen Lab" not in page.title():
        problems.append(f"{path}: title is {page.title()!r}")

    budget = WEIGHT_BUDGET_KB.get(path)
    weight_kb = transferred[0] / 1024
    if budget and weight_kb > budget:
        problems.append(f"{path}: {weight_kb:.0f} KB exceeds the {budget} KB budget")
    print(f"  {path:20s} {weight_kb:7.0f} KB")


def check_anchors(page, problems: list[str]) -> None:
    for path, anchor in ANCHORS:
        page.goto(f"{BASE}/{path}#{anchor}", wait_until="load", timeout=30000)
        page.wait_for_timeout(1200)
        overlap = page.evaluate(HEADER_OVERLAP, anchor)
        if overlap is None:
            problems.append(f"{path}#{anchor}: no such element")
        elif overlap > 0:
            problems.append(
                f"{path}#{anchor}: {overlap}px hidden behind the sticky header"
            )


def main() -> None:
    problems: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        print("page weights")
        for path in PAGES:
            check_page(page, path, problems)
            page.screenshot(
                path=str(SHOTS / f"desktop-{path.replace('.html', '')}.png"),
                full_page=True,
            )

        check_anchors(page, problems)

        page.goto(f"{BASE}/index.html", wait_until="load")
        if MISSION not in page.inner_text("main"):
            problems.append("home is missing the lab mission paragraph")
        for label in ["Research", "Models", "Publications", "News", "People", "Join", "Contact"]:
            page.get_by_role("navigation").get_by_role("link", name=label, exact=True).click()
            page.wait_for_load_state("domcontentloaded")

        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(f"{BASE}/index.html", wait_until="load")
        page.screenshot(path=str(SHOTS / "mobile-home.png"), full_page=True)
        toggle = page.get_by_role("button", name="Menu")
        toggle.click()
        if not page.locator(".nav-bar").evaluate("el => el.classList.contains('open')"):
            problems.append("mobile menu did not open")
        page.keyboard.press("Escape")
        if page.locator(".nav-bar").evaluate("el => el.classList.contains('open')"):
            problems.append("Escape did not close the mobile menu")
        toggle.click()
        page.get_by_role("navigation").get_by_role("link", name="Publications").click()
        page.wait_for_load_state("domcontentloaded")
        page.screenshot(path=str(SHOTS / "mobile-publications.png"), full_page=True)
        browser.close()

    if problems:
        print("\nPROBLEMS")
        for item in problems:
            print("-", item)
        raise SystemExit(1)
    print("\nOK")


if __name__ == "__main__":
    main()

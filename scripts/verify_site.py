#!/usr/bin/env python3
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/Volumes/CrucialX10A/Apps/Website/Shen_Lab")
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
]
MISSION = "The Cardiovascular Precision Medicine Lab is led by Dr. Mengcheng Shen"


def check(page, path: str) -> list[str]:
    problems = []
    page.goto(f"{BASE}/{path}", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(600)
    broken = page.evaluate(
        """() => {
          const urls = [];
          for (const img of document.images) {
            if (!img.complete || img.naturalWidth === 0) urls.push(img.src);
          }
          return urls;
        }"""
    )
    if broken:
        problems.append(f"{path} broken images: {broken}")
    title = page.title()
    if "Shen Lab" not in title:
        problems.append(f"{path} title is {title!r}")
    return problems


def main() -> None:
    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        for path in PAGES:
            problems.extend(check(page, path))
            page.screenshot(
                path=str(SHOTS / f"desktop-{path.replace('.html', '')}.png"),
                full_page=True,
            )
        page.goto(f"{BASE}/index.html", wait_until="domcontentloaded")
        if MISSION not in page.inner_text("main"):
            problems.append("home is missing the lab mission paragraph")
        for label in ["Research", "Models", "Publications", "News", "People", "Join", "Contact"]:
            page.get_by_role("navigation").get_by_role("link", name=label, exact=True).click()
            page.wait_for_load_state("domcontentloaded")
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(f"{BASE}/index.html", wait_until="domcontentloaded")
        page.screenshot(path=str(SHOTS / "mobile-home.png"), full_page=True)
        page.get_by_role("button", name="Menu").click()
        if not page.locator(".nav-bar").evaluate("el => el.classList.contains('open')"):
            problems.append("mobile menu did not open")
        page.get_by_role("navigation").get_by_role("link", name="Publications").click()
        page.wait_for_load_state("domcontentloaded")
        page.screenshot(path=str(SHOTS / "mobile-publications.png"), full_page=True)
        browser.close()
    if problems:
        print("PROBLEMS")
        for item in problems:
            print("-", item)
        raise SystemExit(1)
    print("OK")


if __name__ == "__main__":
    main()

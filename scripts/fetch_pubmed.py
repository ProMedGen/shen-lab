#!/usr/bin/env python3
"""Download PubMed records for Mengcheng Shen into data/publications.json."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path("/Volumes/CrucialX10A/Apps/Website/Shen_Lab")
OUT = ROOT / "data" / "publications.json"

SEARCH = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    "?db=pubmed&retmax=100&term=Shen+Mengcheng%5BAuthor%5D&retmode=json"
)
SUMMARY = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    "?db=pubmed&retmode=json&id="
)


def get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def main() -> None:
    ids = get(SEARCH)["esearchresult"]["idlist"]
    result = get(SUMMARY + ",".join(ids))["result"]
    papers = []
    for pmid in result["uids"]:
        rec = result[pmid]
        doi = next((a["value"] for a in rec.get("articleids", []) if a["idtype"] == "doi"), "")
        authors = [a["name"] for a in rec.get("authors", [])]
        year = int((rec.get("sortpubdate") or rec.get("pubdate") or "0")[:4] or 0)
        papers.append(
            {
                "pmid": pmid,
                "doi": doi,
                "year": year,
                "title": rec.get("title", "").rstrip("."),
                "journal": rec.get("source", ""),
                "authors": authors,
                "volume": rec.get("volume", ""),
                "issue": rec.get("issue", ""),
                "pages": rec.get("pages", ""),
                "pubtype": rec.get("pubtype", []),
            }
        )
    papers.sort(key=lambda p: (-p["year"], p["title"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(papers, indent=2), encoding="utf-8")
    print(f"wrote {len(papers)} papers to {OUT}")


if __name__ == "__main__":
    main()

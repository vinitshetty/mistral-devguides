#!/usr/bin/env python3
"""Build docs/guides.json from the guide folders in this repository.

Runs in CI on every push to main. For each top-level guide directory:

  - parses the front matter of <dir>/index.md
  - validates it against the controlled taxonomy (fails the build on errors)
  - extracts catalog metadata (title, summary, badges, links, cover art)
  - records the last commit date for "newest" sorting

The generated index is committed to docs/guides.json and served by the
GitHub Pages site. Adding a guide is just: create <my-guide>/index.md
with valid front matter and push.

Exit code 1 on any validation error, so bad front matter cannot ship.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "docs" / "guides.json"

# Directories that are not guides.
SKIP_DIRS = {"docs", "scripts", "assets", "_template"}

# Controlled taxonomy (mirrors project.md section 5.3 and house style 7.1).
CONTENT_TYPES = {
    "Quickstart",
    "Community Guide",
    "Partner Guide",
    "Mistral-Certified",
    "Reference Architecture",
}
PRODUCT_CATEGORIES = {
    "Mistral API",
    "AI Studio",
    "Agents",
    "Vibe",
    "Open-weight models",
    "Fine-tuning",
    "Self-deployment",
}
INDUSTRIES = {
    "Financial Services",
    "Legal",
    "Public Sector",
    "Healthcare & Life Sciences",
    "Retail & E-commerce",
    "Manufacturing",
    "Technology",
    "Media",
}

REQUIRED_KEYS = {"id", "language", "categories", "status", "authors", "summary"}
STATUSES = {"Published", "Archived"}

FRONT_MATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.S)
ART_RE = re.compile(r"!\[[^\]]*\]\((assets/[^)\s]+)\)")
H1_RE = re.compile(r"^#\s+(.+)$", re.M)


def parse_front_matter(text: str) -> dict:
    """Parse the flat front matter format used by guides in this repo.

    Supported: `key: value` and indented `- item` lists. Nested mappings are
    not part of the house style; keep front matter flat.
    """
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}
    meta: dict = {}
    key = None
    for line in match.group(1).split("\n"):
        list_item = re.match(r"^\s+-\s+(.*)$", line)
        if list_item and key:
            current = meta.get(key)
            if isinstance(current, list):
                meta[key] = current
            elif current:
                meta[key] = [current]
            else:
                meta[key] = []
            meta[key].append(list_item.group(1).strip())
            continue
        kv = re.match(r"^([^:]+):\s*(.*)$", line)
        if kv:
            key = kv.group(1).strip()
            meta[key] = kv.group(2).strip()
    return meta


def last_commit_date(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out[:10]
    except Exception:
        return ""


def validate(guide_id: str, meta: dict, body: str, errors: list, warnings: list) -> None:
    def err(msg):
        errors.append(f"{guide_id}: {msg}")

    def warn(msg):
        warnings.append(f"{guide_id}: {msg}")

    missing = REQUIRED_KEYS - set(meta)
    if missing:
        err(f"missing required front matter keys: {', '.join(sorted(missing))}")
        return
    if meta["id"] != guide_id:
        err(f"front matter id '{meta['id']}' must match folder name '{guide_id}'")
    if meta["status"] not in STATUSES:
        err(f"status '{meta['status']}' must be one of {sorted(STATUSES)}")
    if not H1_RE.search(body):
        warn("no H1 title found in body")

    cats = meta["categories"] if isinstance(meta["categories"], list) else [meta["categories"]]
    if not any(c in CONTENT_TYPES for c in cats):
        err(f"categories must include one content type from {sorted(CONTENT_TYPES)}")
    for c in cats:
        if c in CONTENT_TYPES or c in INDUSTRIES:
            continue
        root = c.split(">")[0].strip()
        if root in PRODUCT_CATEGORIES:
            if ">" not in c:
                warn(f"product category '{c}' should use 'Root > Feature' form")
            continue
        err(f"unknown category '{c}' (not in the controlled taxonomy)")
    if not meta.get("estimated_time"):
        warn("recommended key 'estimated_time' is missing")
    if not meta.get("level"):
        warn("recommended key 'level' is missing")


def build_guide_entry(guide_id: str, meta: dict, body: str) -> dict:
    cats = [c.strip() for c in (meta["categories"] if isinstance(meta["categories"], list) else [meta["categories"]])]
    title_match = H1_RE.search(body)
    art = ART_RE.search(body)
    return {
        "id": guide_id,
        "title": meta.get("title") or (title_match.group(1).strip() if title_match else guide_id),
        "summary": meta.get("summary", ""),
        "categories": cats,
        "contentType": next((c for c in cats if c in CONTENT_TYPES), "Quickstart"),
        "industries": [c for c in cats if c in INDUSTRIES],
        "products": list(dict.fromkeys(
            c.split(">")[0].strip() for c in cats if c.split(">")[0].strip() in PRODUCT_CATEGORIES
        )),
        "level": meta.get("level", ""),
        "time": meta.get("estimated_time", ""),
        "authors": meta.get("authors", ""),
        "fork": meta.get("fork repo link", ""),
        "platform": meta.get("platform link", ""),
        "language": meta.get("language", "en"),
        "art": f"{guide_id}/{art.group(1)}" if art else "",
        "updated": last_commit_date(REPO_ROOT / guide_id),
    }


def main() -> int:
    errors: list = []
    warnings: list = []
    guides = []

    for entry in sorted(REPO_ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name in SKIP_DIRS or entry.name.startswith("_"):
            continue
        index_md = entry / "index.md"
        if not index_md.exists():
            continue
        text = index_md.read_text(encoding="utf-8")
        meta = parse_front_matter(text)
        body = text[FRONT_MATTER_RE.match(text).end():] if FRONT_MATTER_RE.match(text) else text

        if not meta:
            errors.append(f"{entry.name}: cannot parse front matter in index.md")
            continue
        if meta.get("status") == "Archived":
            print(f"skip archived guide: {entry.name}")
            continue
        validate(entry.name, meta, body, errors, warnings)
        guides.append(build_guide_entry(entry.name, meta, body))

    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    guides.sort(key=lambda g: (g["updated"] or "0000", g["title"]), reverse=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "count": len(guides),
        "guides": guides,
    }
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: wrote {len(guides)} guide(s) to {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

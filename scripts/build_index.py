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

import html
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import markdown

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "docs" / "guides.json"
SITEMAP_PATH = REPO_ROOT / "docs" / "sitemap.xml"
GUIDE_PAGES_DIR = REPO_ROOT / "docs" / "guides"

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


def git_remote_slug():
    """(owner, repo) parsed from the origin remote, or None."""
    try:
        out = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return None
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", out)
    return (m.group(1), m.group(2)) if m else None


def site_base_url() -> str:
    """Published GitHub Pages URL of this repository (project pages layout)."""
    slug = git_remote_slug()
    if not slug:
        return ""
    owner, repo = slug
    if repo == f"{owner}.github.io":
        return f"https://{repo}/"
    return f"https://{owner}.github.io/{repo}/"


def raw_base_url() -> str:
    """Base URL of guide assets on raw.githubusercontent.com."""
    slug = git_remote_slug()
    if not slug:
        return ""
    owner, repo = slug
    return f"https://raw.githubusercontent.com/{owner}/{repo}/main/"


SHELL_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Mistral Developer Guides</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
{og_image}<link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{jsonld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="../../assets/site.css?v=4">
</head>
<body data-guide-id="{guide_id}">

<div class="progress" id="progress"></div>

<header class="topbar">
  <a class="brand" href="../../index.html">
    <span class="brand-mark">M</span>
    <span class="brand-name">MISTRAL <em>DEVELOPER GUIDES</em></span>
  </a>
  <div class="reader-actions">
    <a class="btn" id="fork-btn" href="{fork}" target="_blank" rel="noopener" style="{fork_style}"><svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><circle cx="4" cy="3" r="1.75"/><circle cx="12" cy="3" r="1.75"/><circle cx="8" cy="13" r="1.75"/><path d="M4 4.75v1.5c0 1.5 1.5 3 4 3s4-1.5 4-3v-1.5"/><path d="M8 9.25v2"/></svg>Fork Repo</a>
    <a class="btn accent" href="https://console.mistral.ai" target="_blank" rel="noopener">Open in Mistral Console</a>
  </div>
</header>

<main class="reader">
  <article class="markdown-body" id="content" data-prerendered="1">
    <div class="guide-head">
      <span class="kicker">{kicker}</span>
      <h1>{title}</h1>
      <div class="sub">{description}</div>
      <div class="byline">{byline}</div>
    </div>
{body_html}
  </article>
  <aside class="rail">
    <h4>On this page</h4>
    <nav id="toc"></nav>
    <div class="rail-cta">
      <p>Ready to build?</p>
      <a class="btn accent" id="console-cta" href="{platform}" target="_blank" rel="noopener" style="display:block;text-align:center">Open in Mistral Console</a>
    </div>
  </aside>
</main>

<footer>
  <span>Spot an issue? <a href="https://github.com/vinitshetty/mistral-devguides/issues">File feedback</a> or open a PR.</span>
  <nav>
    <a href="../../index.html">All guides</a>
    <a href="https://docs.mistral.ai">Docs</a>
    <a href="https://github.com/vinitshetty/mistral-devguides">GitHub</a>
  </nav>
</footer>

<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="../../assets/site.js?v=5"></script>
</body>
</html>
"""

PNG_ART_RE = re.compile(r"!\[[^\]]*\]\((assets/[^)\s]+\.(?:png|jpe?g))\)")


def render_body(body: str, guide_id: str, raw_base: str) -> str:
    """Markdown to HTML for the static page: resolve asset paths against the
    repo and drop the leading H1 (the page header already renders the title)."""
    body = re.sub(r"\]\((assets/[^)]+)\)", lambda m: f"]({raw_base}{guide_id}/{m.group(1)})", body)
    body = H1_RE.sub("", body, count=1)
    return markdown.markdown(body, extensions=["fenced_code", "tables"])


def guide_shell(guide: dict, body: str, base_url: str, raw_base: str) -> str:
    """Fully pre-rendered static page for one guide; site.js only enhances."""
    canonical = f"{base_url}guides/{guide['id']}/"
    author_name = re.match(r"([^(]+)", guide.get("authors", "")).group(1).strip()
    og_image_match = PNG_ART_RE.search(body)
    og_image_url = f"{raw_base}{guide['id']}/{og_image_match.group(1)}" if og_image_match else ""
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": guide["title"],
        "description": guide.get("summary", ""),
        "url": canonical,
        **({"image": og_image_url} if og_image_url else {}),
        **({"dateModified": guide["updated"]} if guide.get("updated") else {}),
        **({"author": {"@type": "Person", "name": author_name}} if author_name else {}),
    }, ensure_ascii=False)
    byline = "".join(
        f'<span>{html.escape(part)}</span>'
        for part in (
            f"by {guide['authors']}" if guide.get("authors") else "",
            guide.get("level", ""),
            guide.get("time", ""),
        )
        if part
    )
    return SHELL_TEMPLATE.format(
        title=html.escape(guide["title"], quote=True),
        description=html.escape(guide.get("summary", ""), quote=True),
        canonical=html.escape(canonical, quote=True),
        og_image=(
            f'<meta property="og:image" content="{html.escape(og_image_url, quote=True)}">\n'
            if og_image_url else ""
        ),
        jsonld=jsonld.replace("</", "<\\/"),
        guide_id=html.escape(guide["id"], quote=True),
        kicker=html.escape(guide.get("contentType", ""), quote=True),
        byline=byline,
        body_html=render_body(body, guide["id"], raw_base),
        fork=html.escape(guide.get("fork") or "https://github.com/vinitshetty/mistral-devguides", quote=True),
        fork_style="" if guide.get("fork") else "display:none",
        platform=html.escape(guide.get("platform") or "https://console.mistral.ai", quote=True),
    )


def write_sitemap(guides: list, base_url: str) -> None:
    entries = [
        f"  <url><loc>{base_url}</loc></url>",
        *(
            f"  <url><loc>{base_url}guides/{g['id']}/</loc>"
            + (f"<lastmod>{g['updated']}</lastmod>" if g.get("updated") else "")
            + "</url>"
            for g in guides
        ),
    ]
    SITEMAP_PATH.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries) + "\n</urlset>\n",
        encoding="utf-8",
    )


def write_guide_pages(guides: list, base_url: str, raw_base: str) -> None:
    for g in guides:
        page_dir = GUIDE_PAGES_DIR / g["id"]
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(
            guide_shell(g, g["_body"], base_url, raw_base), encoding="utf-8"
        )


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
        guides.append({**build_guide_entry(entry.name, meta, body), "_body": body})

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
        "guides": [{k: v for k, v in g.items() if k != "_body"} for g in guides],
    }
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: wrote {len(guides)} guide(s) to {OUTPUT_PATH.relative_to(REPO_ROOT)}")

    base_url = site_base_url()
    raw_base = raw_base_url()
    if base_url and raw_base:
        write_sitemap(guides, base_url)
        write_guide_pages(guides, base_url, raw_base)
        print(f"OK: wrote sitemap and {len(guides)} guide page(s) under {GUIDE_PAGES_DIR.relative_to(REPO_ROOT)}/")
    else:
        print("WARNING: could not determine Pages URL from git remote; skipped sitemap and guide pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())

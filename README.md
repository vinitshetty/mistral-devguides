# Mistral Developer Guides

Hands-on tutorial library for building with Mistral AI. The catalog lives at
**https://vinitshetty.github.io/mistral-devguides/** and renders guide content
straight from this repo.

## Adding a guide (the whole process)

1. Copy `_template/` to a new folder named after your guide id
   (lowercase, hyphenated, e.g. `rag-chatbot/`).
2. Fill in the front matter and write the guide as Markdown in `index.md`.
   Put images/diagrams in an `assets/` folder next to it.
3. Open a PR against `main`.

That is it. CI validates the front matter, regenerates `docs/guides.json`, and
GitHub Pages redeploys - your guide appears in the catalog automatically.

## Front matter contract (validated in CI)

| Key | Required | Notes |
|---|---|---|
| `id` | yes | Must match the folder name |
| `language` | yes | ISO code, e.g. `en` |
| `categories` | yes | Controlled taxonomy (see below) |
| `status` | yes | `Published` or `Archived` |
| `authors` | yes | `Full Name (github-handle)` |
| `summary` | yes | One sentence for the catalog card |
| `estimated_time` | recommended | e.g. `45 minutes` |
| `level` | recommended | `Beginner` / `Intermediate` / `Advanced` |
| `fork repo link` | recommended | The guide's runnable code repo |
| `platform link` | recommended | Deep link into the Mistral Console |
| `feedback link` | optional | Where readers report issues |

Front matter must stay flat: `key: value` lines and `- item` lists only.

## Controlled taxonomy

- **Content type:** Quickstart - Community Guide - Partner Guide - Mistral-Certified - Reference Architecture
- **Product category (as `Root > Feature`):** Mistral API - AI Studio - Agents - Vibe - Open-weight models - Fine-tuning - Self-deployment
- **Industry:** Financial Services - Legal - Public Sector - Healthcare & Life Sciences - Retail & E-commerce - Manufacturing - Technology - Media

Authors select from this list; CI rejects unknown categories. To evolve the
taxonomy, change `scripts/build_index.py` and `docs/assets/site.js` together.

## Repository layout

```
my-guide/
  index.md      the guide (front matter + Markdown)
  assets/       images and diagrams
_template/      starter for new guides (ignored by the build)
scripts/build_index.py   validates guides, generates docs/guides.json
docs/          GitHub Pages site (catalog + reader)
.github/workflows/build-index.yml   CI pipeline
project.md     platform blueprint and house style
```

Guides with runnable code keep the code in its **own repository** (one repo
per guide, e.g. [invoice-automation](https://github.com/vinitshetty/invoice-automation))
and link it via the front-matter `fork repo link`. The content repo stays
light; a fork of the code repo gives readers a clean working project.

## Local preview

```bash
python3 scripts/build_index.py        # validate + regenerate the index
cd docs && python3 -m http.server 8123 # then open http://localhost:8123
```

House style and authoring conventions live in `project.md` (section 7).

# Project: Developer Guides Platform ("Quickstarts") — Blueprint from Snowflake, Adapted for Mistral

> Reference platform: https://www.snowflake.com/en/developers/guides/
> Goal: build the equivalent platform for Mistral AI ("Mistral Developer Guides").

---

## 1. The Whole Idea

Snowflake Developer Guides is a **self-serve, hands-on tutorial library** for developers, maintained on the
corporate website but **authored in Markdown in a public GitHub repository**. It is not documentation in
the classic reference sense — docs tell you *what* an API is; guides show you *how to build something real,
end to end, today*.

The core idea is a **content flywheel**:

```
   Snowflake DevRel + partners + community authors
              │  write Markdown guides in a public repo
              ▼
   PR → automated checks → preview link → DevRel review → publish to site
              ▼
   675+ searchable, filterable, step-by-step tutorials
              ▼
   Readers build something real (code included, never pseudo-code)
              ▼
   Readers become authors → contribute back via GitHub
```

Three properties make it work:

1. **Build-first guarantee.** Every guide commits to the reader having *built* something by the end.
   Actual runnable code is mandatory — concepts and pseudo-code are rejected.
2. **GitHub-native authoring.** Guides are plain Markdown files with a metadata header, stored in
   `Snowflake-Labs/sfguides`. Anyone can fork, edit, preview, and submit a PR. Publishing is a PR
   review, not a CMS workflow.
3. **Faceted discovery.** Every guide is tagged along four independent axes (content type, industry,
   product category, product feature) so the same content serves a data engineer, an industry
   architect, and a partner Solutions Engineer from one landing page.

## 2. Objective

- **Primary objective:** get any developer from "heard of the product" to "built a working thing"
  in a single session, without talking to sales.
- **Secondary objectives:**
  - Provide **reference architectures** and **best practices**, not just feature tours.
  - Give **partners and community** a certified channel to publish solutions (with badges:
    Quickstart / Community Solution / Partner Solution / Certified Solution / Well-Architected
    Framework).
  - Serve **industry-specific** entry points (Financial Services, Healthcare, Public Sector, etc.)
    so the same tutorial library doubles as vertical go-to-market content.
  - Drive an ongoing contribution flywheel (users file issues and PRs to fix outdated guides).
  - Feed the wider developer ecosystem: community forums, docs, engineering blog, YouTube, events,
    open-source repos, and training/certification are all cross-linked from the hub.

## 3. Platform Structure

### 3.1 Site hierarchy

```
Developers hub (/developers/)
├── Overview            — hero, featured guides, solution pillars, industry guides,
│                         community/docs/open-source/blog/event links
├── Guides              — THE tutorial library (this project's core)
├── Open Source         — projects the company maintains/supports
├── Learn               — courses, self-paced training, certifications
├── Developer Blog      — engineering-authored posts
├── Events              — user groups, virtual hands-on labs (VHOL), summits
└── Downloads           — CLIs, drivers, SDKs, libraries
```

### 3.2 Guides landing page (the catalog)

- **Hero + value promise:** "Discover product quickstarts, industry-specific use-cases, administration
  best practices and reference architectures from Snowflake experts and partners."
- **Faceted search over ~675 guides** with four filter axes:
  - **Content type:** Quickstart · Community Solution · Partner Solution · Certified Solution ·
    Well-Architected Framework
  - **Industry:** Advertising/Media/Ent · Financial Services · Healthcare & Life Sciences ·
    Manufacturing · Public Sector · Retail & CPG · Technology · Telecom · Travel & Hospitality
  - **Product category:** Platform · Analytics · AI · Applications & Collaboration · Data Engineering
  - **Product feature:** fine-grained tags (e.g., Cortex Analyst, Notebooks, Snowpark, Horizon,
    Apache Iceberg, Streamlit, Native App Framework…)
- **Card grid** with title, date, and feature badges; **sort** (newest/oldest, A–Z/Z–A) and pagination.
- **Featured content strip** at top (e.g., "Getting Started with your first Notebook").
- **Industry Guides** section — one curated page per vertical.
- **Footer loop:** Docs · Guides · Engineering Blog · newsletter subscription.

### 3.3 Anatomy of a single guide (the template)

Every guide page is a **step-by-step reader** with a right-column step menu and auto-saved progress:

```markdown
---
id: getting-started-with-snowflake          # lowercase, hyphenated, must match
language: en                                 # en | es | it | fr | ja | ko | pt_br
categories: <taxonomy paths>                 # content type + category1/2/3 + industry
status: Published                            # Published | Archived (no hidden)
authors: Full Name (github-login)
summary: One sentence shown on the landing page.
feedback link: <github issues url>
fork repo link: <repo for the guide's code>
environments: web                            # or a specific event
---

## Overview
### Prerequisites        # what to know/have before starting
### What You'll Learn    # bulleted outcomes
### What You'll Need     # accounts, tools, trial signup
### What You'll Build    # the concrete artifact produced

## <Hands-on steps>       # one H2 per step; H3/H4 for sub-steps (never beyond H4)

## Conclusion & Resources
### What You've Learned  # recap
### Resource Links       # docs, blogs, videos, repos
```

Rules that keep quality consistent:

- H2 headings are short (3–4 words) and form the step menu.
- **No HTML in Markdown** — pure Markdown only (tables, images, links, videos, code blocks,
  callout/info boxes, download buttons).
- Images: lowercase-hyphenated filenames, web-optimized, max ~1 MB, stored in a flat `assets/`
  folder next to the guide.
- The reader must end with a **working build**, so real code is mandatory.

### 3.4 Authoring & publishing pipeline

```
Author experience:
Fork repo → write .md + assets → open PR
   → automated checks (id format, id = filename = folder, language/category codes valid)
   → bot comments an auto-generated preview link on the PR
   → DevRel team reviews & approves
   → published to site within ~1 hour

Reader experience:
Open guide → step-by-step pages with progress auto-saved → copy code / fork the repo
→ fix typos or outdated content via PR or GitHub issues
```

Governance: strict controlled taxonomy — **authors may not invent new tags, categories, or content
types**; they select from the published list. Outdated guides get updated rather than archived
(archiving is a last resort due to redirects).

### 3.5 Ecosystem hooks (usability glue)

- Guides carry a **"Fork Repo"** button (code lives beside the tutorial) and an
  **"Open in product"** deep link.
- Guides are promoted as **instructor-led Virtual Hands-on Labs** (same content, live teaching).
- Cross-links to forums/community, docs, open-source org, engineering blog, YouTube channel,
  GitHub, training & certifications, and a monthly newsletter.

## 4. Usability — why it works

| Audience | What they get | How the platform serves them |
|---|---|---|
| New developer | First-session win | "Getting started" quickstarts, free-trial onboarding, prerequisites spelled out |
| Practitioner (dev/DS/MLE) | Solutions to job-to-be-done | Faceted search by product feature; runnable code in the guide + forkable repo |
| Architect | Reference architectures | Well-Architected / Reference Architecture content type; industry guides |
| Partner / SI | A certified showcase | Partner Solution badge + published co-branded tutorial |
| Community author | Contribution path | Fork → PR → review → publish; issues for fixes |
| Field/marketing | Vertical GTM content | Same library, industry-faceted entry pages |

Key usability decisions worth copying:

1. **Progress persistence** — the reader's position in a multi-step tutorial is auto-saved.
2. **Single source, many lenses** — one Markdown corpus, four filter axes, industry landing pages.
3. **Trust badges** — content-type labels tell readers who vouches for the content.
4. **Fork-first** — every guide has a repo; readers get code, authors get contributions.
5. **Cheap authoring** — Markdown + GitHub preview; no CMS, no engineering ticket for publishing.

---

## 5. Mistral Adaptation: "Mistral Developer Guides"

### 5.1 Concept

A hands-on tutorial library at `mistral.ai/developers/guides` where anyone can learn to **build with
Mistral AI** — Mistral APIs, Agents, open-weight models, and deployments — by completing
runnable, end-to-end guides that produce a working artifact.

### 5.2 Objective

- Convert a curious visitor into a builder in one session using the Mistral free API tier.
- Showcase the breadth of the stack through runnable examples rather than feature lists.
- Give the community, partners, and DevRel one shared, versioned publishing channel.
- Provide industry/vertical recipes (legal, finance, public sector, retail, support automation).

### 5.3 Proposed structure

```
Developers hub (mistral.ai/developers)
├── Overview          — hero, featured guides, solution pillars
├── Guides             — the tutorial library (core deliverable)
├── Open Source        — mistralai/* GitHub org (clients, examples, evals)
├── Learn              — notebooks, courses, certifications
├── Developer Blog     — engineering posts
├── Events             — hackathons, office hours, meetups
└── Downloads          — Python/JS SDKs, Codestral IDE plugins, vLLM/TensorRT-LLM recipes
```

**Guide catalog facets** (adapted taxonomy):

- **Content type:** Quickstart · Community Guide · Partner Guide · Mistral-Certified · Reference Architecture
- **Product category:**
  - Mistral API (Chat Completions, OCR, Embeddings, Moderation, Batch)
  - Agents (Agent Builder, Agents API, tools/function calling, MCP)
  - Vibe (assistants, Deep Research, Canvas, connectors)
  - Open-weight models (Mistral Large/Medium/Small, Ministra, Codestral, Devstral, Mathstral,
    Voxtral, Magistral, Pixtral)
  - Fine-tuning & customization (API fine-tuning, evals, prompt libraries)
  - Self-deployment & enterprise (vLLM, TensorRT-LLM, Sagittarius, on-prem, edge)
- **Feature tags:** function calling, structured JSON output, RAG, web search, code execution,
  vision/OCR, TTS/ASR, embeddings, guardrails/moderation, streaming, batch API, quantization
- **Industry:** Financial Services · Legal · Public Sector · Healthcare & Life Sciences ·
  Retail & E-commerce · Manufacturing · Technology · Media
- **Language:** en, fr, es, de, it, ja, ko, pt_br, hi

**Seed guide list (~15 to launch):**

1. Getting Started with the Mistral Chat API (Python + JS, streaming, free tier)
2. Your First Mistral Agent (Agent Builder + Agents API, tools, memory)
3. Function Calling for Reliable Structured Output (JSON schema, validation)
4. Building a RAG Chatbot with Mistral Embeddings + OCR (PDF ingestion to answer)
5. Fine-tuning Mistral Small for Domain Tasks via the Mistral Console
6. Self-Hosting Mistral Small with vLLM on a Single GPU
7. Code Generation with Codestral in Your IDE (plugins + API)
8. Agentic Coding with Devstral in a Terminal Sandbox
9. Multimodal Document Pipelines with Mistral OCR
10. Voice Applications with Voxtral (ASR/TTS recipes)
11. Guardrails: Moderation + Prompt Guard in Production
12. Batch Processing Millions of Requests with the Batch API
13. Reasoning Workflows with Magistral
14. MCP Servers + Mistral Agents
15. Cost & Latency Optimization: routing between Mistral Large/Medium/Small

### 5.4 Guide template (same contract as Snowflake's)

```markdown
---
id: mistral-first-agent        # lowercase, hyphenated, matches filename & folder
language: en
categories: <taxonomy paths>   # content type + product category + industry
status: Published              # Published | Archived
authors: Full Name (github-login)
summary: One sentence for the catalog card.
feedback link: https://github.com/mistralai/devguides/issues
fork repo link: <guide's code repo>
platform link: <deep link into the Mistral Console>
---

## Overview
### Prerequisites
### What You'll Learn
### What You'll Need       # Mistral account + API key, free-tier notes, SDK install
### What You'll Build

## <Hands-on steps>          # runnable code in every step

## Conclusion & Resources
### What You've Learned
### Resource Links
```

### 5.5 Publishing pipeline

- Public repo `mistralai/devguides`: one folder per guide (`<id>/index.md` + `assets/`).
- CI on PR: metadata schema validation (id/filename/folder match, taxonomy codes from a controlled
  list, language code), Markdown lint, image size checks, code-block language tags.
- Bot posts a **preview URL** on each PR; DevRel review; merge → auto-deploy within the hour.
- Every guide auto-gets a **"Fork Repo"** button and an **"Open in Mistral Console"** deep link.
- Issues-based reader feedback; stale guides are updated, not archived.

### 5.6 Usability targets (acceptance criteria)

- A reader completes a "Getting Started" guide in **under 20 minutes** using only the free tier.
- Any guide is reachable via **≤2 facet selections** from the catalog.
- Reader progress auto-saves; the right-rail step menu always shows position.
- Authors need **no tooling beyond GitHub** and a Markdown preview.
- All guide code is **runnable from the forked repo** with a documented one-command setup.

### 5.7 Success metrics

- Guides published and contribution rate (external PRs/issues per month)
- Completion rate (progress-saved-to-final-step) and time-to-complete
- Free-tier signups and API-key creation attributed to guide traffic
- Facet usage (which product categories and industries pull most)
- Repo stars/forks and community-guide share vs. DevRel-authored share

---

## 6. Recommended Content Flow for a Quickstart

> Derived from a structural analysis of 52 randomly sampled Snowflake guides
> (from the 788 in the source repo): heading sequences, section presence,
> length, and code-block counts.

### 6.1 What the data shows

| Metric (n=52) | Value |
|---|---|
| Word count | median ~2,100 (range 400–5,500) |
| H2 steps | median 8 (range 2–25) |
| Code blocks | median 11 (range 0–28) |
| Opens with "## Overview" | 100% of quickstarts |
| Has Prerequisites | ~85% |
| Has "What You'll Learn" | ~85% |
| Has "What You'll Build" | ~75% |
| Has "What You'll Need" | ~65% |
| Has Conclusion & Resources | ~80% |
| Has Troubleshooting section | <10% |
| Has Cleanup section | ~20% |

The strongest guides share an arc: **orient → set up → first success fast →
build in layers with verify checkpoints → recap → next steps.**

### 6.2 The recommended flow

```
Metadata / catalog card        title, 1-line summary, time estimate, tags
─────────────────────────────────────────────────────────────────────
## Overview                    2–3 sentence hook: the problem, the artifact
### Prerequisites              skills assumed + accounts/keys needed
### What You'll Learn          4–7 outcome bullets (future tense)
### What You'll Need           checklist with links (free tier, API key, SDK)
### What You'll Build          concrete artifact + screenshot/architecture
─────────────────────────────────────────────────────────────────────
## Set Up Your Environment     installs, credentials, project scaffold
## <First Success>             smallest runnable call — output within ~10 min
## <Build: 2–5 verb-first H2 steps, each with>
   • 1–3 sentence intro (what + why)
   • runnable code block
   • expected output
   • "Verify" / checkpoint sub-step
## <Extend> (optional)         one advanced variation or production concern
## Troubleshooting (optional)  top 3–5 real errors + fixes
## Cleanup (optional)          only if the guide creates billable resources
─────────────────────────────────────────────────────────────────────
## Conclusion and Resources
### What You Learned           mirrors the Learn bullets (past tense)
### What You Accomplished      restate the artifact, link to final code
### Next Steps                 1–3 deeper guides to continue to
### Related Resources          docs, blog posts, repo, model pages
```

### 6.3 Rules of thumb

- **H2 count:** 6–10. More than ~10 splits the step menu; fewer than 4 means
  steps are too coarse for progress tracking.
- **Headings:** verb-first, 3–4 words ("Deploy the API", "Create the Agent").
  Use `Step 1:`/`Step 2:` prefixes only inside a single setup phase.
- **First success within 10 minutes** of reading — one runnable call that
  prints/returns something before any complex config.
- **Verify after every meaningful step.** The best guides never leave more
  than one code block between checkpoints.
- **Explain "why", not just "what"** — the top guides include one-line
  rationale callouts ("Why a dedicated demo user?") before non-obvious choices.
- **Every code block runnable as-is** — full commands, real values, copy-paste
  friendly. No pseudo-code.
- **Conclusion is mandatory.** ~20% of sampled guides just stop; those read as
  unfinished. End with a recap that mirrors the opening promise.
- **Target size:** 1,500–3,000 words, 8–15 code blocks. Under 1,000 words is a
  stub; over 4,000 should be split into a series.
- **Optional sections are conditional, not filler:** Troubleshooting only when
  setup can realistically fail; Cleanup only when resources cost money.

### 6.4 Worked example — "Build Your First Mistral Agent"

```
Metadata: quickstart · Mistral API · Agents · 45 min · en
## Overview
### Prerequisites      — Python 3.10+, a Mistral account (free tier works)
### What You'll Learn  — create an agent, attach tools, run a multi-turn task,
                         inspect traces, deploy via API
### What You'll Need   — API key from console (link), mistralai SDK (pip install)
### What You'll Build  — a support-triage agent that classifies tickets and
                         drafts replies, callable via the Agents API
## Create the Agent   — console or agents.create() + screenshot
## First Success      — one chat completion through the agent; expected JSON out
## Add Tools          — web search + a custom function (code, then verify)
## Run the Task       — multi-turn conversation loop (code, trace output, verify)
## Call It from Code  — Agents API request with polling (code + expected output)
## Troubleshooting    — 401 (bad key), tool-call loops, rate limits
## Conclusion and Resources
### What You Learned  — mirror of the Learn bullets
### Next Steps        — RAG guide, function-calling guide, MCP guide
### Related Resources — Agents API docs, cookbook repo, model page
```

---

## 7. House Style & Authoring Preferences

> Conventions agreed while producing the first guide ("The Invoice Automation Lab").
> These apply to every guide in this repo, alongside the template in section 5.4
> and the content flow in section 6.

### 7.1 Terminology

- Say **Mistral Console** (console.mistral.ai). Never "La Plateforme" — retired brand.
- The chat product is **Vibe** (vibe.mistral.ai). Never "Le Chat" — retired brand.
- Current naming: **Mistral API** (the HTTP API), **AI Studio** (the console workbench),
  **Vibe** (the chat product).
- Front-matter taxonomy follows the same rule — e.g. `Mistral API > OCR`, never
  `La Plateforme > ...`.

### 7.2 Tone and length

- Concise beats complete. Target **1,500–2,000 words** for a single-session lab;
  if a paragraph can be one sentence, make it one sentence.
- Checkpoints are single sentences.
- Guides may be playful in framing (labs, challenges, crash tests) but never wordy.
- Longer guides split into **Part sections** (`## Part 1 — ...`, `## Part 2 — ...`)
  with verb-first H3 steps inside — one guide, one repo, one flow
  (see "The Invoice Automation Lab" for the Exploration/Automation pattern).

### 7.3 Visuals

- A guide earns visuals only when they show something the reader will see on
  their own screen (real product UI) or explain structure (diagrams).
- **Never embed screenshots of documentation pages** — link to them instead.
- Architecture/flow diagrams (SVG, flat `assets/` folder) are the preferred visual.

### 7.4 Links

- Verify every external link returns HTTP 200 before publishing.
- docs.mistral.ai slugs use **underscores**: `your_first_workflow`, `core_concepts`,
  `cookbook_examples`, `waiting_for_conditions`. Never guess a slug from a title —
  pull it from `https://docs.mistral.ai/sitemap.xml`.

### 7.5 Toolchain notes (mistralai-workflows 3.15)

- SDK: `uv add mistralai-workflows` → `import mistralai.workflows as workflows`;
  requires Python >= 3.12.
- The `mistralai` client is a PEP 420 namespace package:
  `from mistralai.client import Mistral` (not `from mistralai import Mistral`).
- Executions are triggered/controlled through `Mistral().workflows` and
  `.workflows.executions` client groups; the standalone `WorkflowsClient` is gone.
- Signal `input` must be a plain dict, not a pydantic model.
- Activity-only imports must sit inside `with workflow.unsafe.imports_passed_through():`
  or worker registration fails sandbox determinism validation.
- Workers require `DEPLOYMENT_NAME` in the environment; it doubles as the task queue.

### 7.6 Production workflow for guides

1. Draft in `<id>/index.md` + `assets/` per sections 5.4 and 6.2.
2. **Live-test every command and code block**; paste real outputs, never invented ones.
3. Review with the author in chat, revise, then commit and push to GitHub for
   final review on the platform.
4. Before making anything public, scan git history for secrets
   (API keys live only in gitignored `.env` files).

### 7.7 Site, CI and the catalog

- The site is GitHub Pages from `docs/` on `main` — no external hosting.
- The catalog reads `docs/guides.json`, regenerated by CI
  (`.github/workflows/build-index.yml` → `scripts/build_index.py`) on every push.
- CI validates front matter against the controlled taxonomy and **fails the
  build** on errors; unknown categories never reach the catalog.
- Adding a guide = copy `_template/`, fill in front matter, push to `main`.
  The catalog picks it up automatically. Never hand-edit `docs/guides.json`.
- Guide pages render their `index.md` live from the repo at view time, so
  content is always current even between catalog builds.

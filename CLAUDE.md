# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development

```bash
# Start Flask (debug) + Tailwind (watch) in one terminal:
bash run-it.sh
# Site at http://127.0.0.1:5000

# Build static site for deploy:
npm run css:build && python freeze.py
# Output in build/
```

Requires Python 3.11+ (via `uv`), Node 20+. `run-it.sh` creates a `.venv`, installs deps, and launches both processes.

## Architecture

Flask + MyST essayist site, frozen to static HTML via Frozen-Flask, deployed on Netlify (`main` branch).

**Content pipeline:** MyST Markdown files (`.myst`) with YAML frontmatter in `content/` are parsed at request time by `app.py` using `myst-parser` + `docutils`, rendered to HTML, and injected into Jinja templates.

**i18n:** All URLs are language-prefixed (`/<lang>/...`). Languages (`en`, `fr`), default, and UI strings live in `i18n.py`. `/` redirects to the default language. Content is mirrored under `content/<lang>/`.

**Content types and routes:**
- `content/<lang>/essays/*.myst` — date-sorted essays. Index at `/<lang>/`, detail at `/<lang>/<slug>/`
- `content/<lang>/projects/*.myst` — projects sorted by `status` (active/shipped/archived). Index at `/<lang>/work/`, detail at `/<lang>/work/<slug>/`
- `content/<lang>/pages/*.myst` — standalone pages (about, etc.) served at `/<lang>/<slug>/` as a fallback after essays
- `/<lang>/feed.xml` — Atom feed of essays

The `essay` route handler tries essays first, then falls through to pages — both share the `/<lang>/<slug>/` URL pattern.

**Styling:** Tailwind CSS with Solarized light color palette defined as semantic roles in `tailwind.config.js` (ink, paper, rule, action, accent, brand, etc.). Uses `@tailwindcss/typography` for prose. Fonts: Source Serif 4 (body), Inter (meta/UI), JetBrains Mono (code).

**Static build:** `freeze.py` crawls all Flask routes and writes flat HTML to `build/`. Netlify runs this via `netlify.toml`.

## Content frontmatter

Essays require `title` and `date` (YYYY-MM-DD). Projects use `title` and `status`. Pages need at minimum `title`.

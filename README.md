# consultant-website

Flask + MyST essayist site, frozen to static HTML via Frozen-Flask and deployed on Netlify.

## Stack

- **Flask** routes + Jinja templates
- **MyST Markdown** content (`.myst`) with YAML frontmatter, parsed via `myst-parser` + `docutils`
- **Tailwind CSS** + `@tailwindcss/typography` for prose styling
- **Frozen-Flask** generates static HTML into `build/`
- **Netlify** builds and serves the static output

## Layout

```
app.py                 Flask routes + MyST rendering
i18n.py                Languages, default, UI strings
freeze.py              Frozen-Flask generators
content/
  en/, fr/
    essays/*.myst      Date-sorted essays
    projects/*.myst    Projects (status: active/shipped/archived)
    pages/*.myst       Standalone pages (about, etc.)
templates/
  base.html            Shell
  index.html           Essays index
  essay.html           Essay detail
  page.html            Standalone page
  work_index.html      Projects index
  project.html         Project detail
  feed.xml             Atom feed
  404.html
  _partials/           Shared chunks
static/
  css/input.css        Tailwind entry
  css/site.css         Built (gitignored)
  img/, favicon.ico
netlify.toml           Build config
tailwind.config.js     Semantic color tokens (Solarized light)
run-it.sh              Dev launcher
package.json           Tailwind deps
requirements.txt       Python deps
pyproject.toml         Python project metadata
```

Requires Python 3.11+ (via `uv`) and Node 20+.

## Dev

```bash
bash run-it.sh
# Flask (debug) + Tailwind (watch), site at http://127.0.0.1:5000
```

`run-it.sh` creates `.venv`, installs Python and Node deps, then runs Tailwind in watch mode alongside the Flask dev server.

## Build (static)

```bash
npm run css:build && python freeze.py
# Output: build/
```

## Content

Drop `.myst` files into `content/<lang>/{essays,projects,pages}/` with YAML frontmatter:

```markdown
---
title: On distribution
date: 2026-03-27
---

Body in MyST Markdown.
```

Frontmatter requirements:
- **Essays** — `title`, `date` (YYYY-MM-DD)
- **Projects** — `title`, `status` (`active` | `shipped` | `archived`)
- **Pages** — `title`

## Routes

- `/` — redirects to the default language (`en`)
- `/<lang>/` — essays index (grouped by year)
- `/<lang>/<slug>/` — essay; falls through to a page if no essay matches
- `/<lang>/work/` — projects index (sorted by status)
- `/<lang>/work/<slug>/` — project detail
- `/<lang>/feed.xml` — Atom feed

## i18n

Two languages: `en` (default) and `fr`. Declared in `i18n.py` alongside UI strings. Add a language by extending `LANGS` and `STRINGS`, then mirror the `content/<lang>/` tree.

## Deploy

Netlify is wired to the `main` branch. `netlify.toml` installs Python + Node deps, builds Tailwind, freezes the site, and publishes `build/`.

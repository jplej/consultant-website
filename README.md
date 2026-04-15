# consultant-website

Flask + Jinja + htmx + Tailwind (with `@tailwindcss/typography`), built to a static site via Frozen-Flask and deployed on Netlify.

## Stack

- **Flask** routes + Jinja templates
- **Markdown** content in `content/` with YAML frontmatter (`python-frontmatter`)
- **Tailwind CSS** + **@tailwindcss/typography** for prose styling
- **htmx** for progressive interactivity
- **Frozen-Flask** to generate static HTML into `build/`
- **Netlify** hosts the static output

## Layout

```
app.py                 Flask routes
freeze.py              Static site generator (Frozen-Flask)
content/
  pages/               About, Contact, etc. (*.md)
  services/            Service detail pages (*.md)
templates/
  base.html            Shell (header/footer, CSS, htmx)
  index.html           Landing
  page.html            Generic markdown page
  service.html         Service detail
  404.html
  _partials/           header.html, footer.html
static/
  css/input.css        Tailwind entry
  css/site.css         Built (gitignored)
netlify.toml           Build config
tailwind.config.js
package.json           tailwind + typography
requirements.txt       Python deps
```

## Dev

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
npm install

# One command: Flask (debug) + Tailwind watch + live reload
LIVETW_ENV=development livetw dev
```

Visit the URL printed in the terminal. Edits to `.py`, templates, Markdown, or Tailwind classes hot-reload the browser; CSS swaps without a full page refresh.

## Build (static)

```bash
npm run css:build
python freeze.py
# output: build/
```

## Content

Drop `*.md` files into `content/pages/` or `content/services/` with frontmatter:

```markdown
---
title: Strategy
summary: Short description for cards and SEO.
---

Body in Markdown.
```

Routes:
- `/` — landing (lists all services)
- `/<slug>/` — any file under `content/pages/`
- `/services/<slug>/` — any file under `content/services/`

## Deploy

Netlify is wired to the `main` branch via the GitHub app. `netlify.toml` installs Python + Node deps, builds Tailwind, freezes the site, and publishes `build/`.

## i18n (later)

English only for now. Plan: URL prefix scheme (`/en/...`, `/fr/...`) via a simple locale-aware route factory when French content is added.

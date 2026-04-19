import hashlib
import html
import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KROKI_URL = "https://kroki.io/mermaid/svg"
DIAGRAM_DIR = Path(__file__).parent / "static" / "img" / "diagrams"
_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
_ALT_RE = re.compile(r"^\s*%%\s*alt:\s*(.+?)\s*$", re.MULTILINE)

# Solarized (Ethan Schoonover). Mirror the site's semantic roles.
# Ink linework + rule-tinted node fills, no panel bg, transparent.
# Reads like typeset figures in the essay. The yellow note border is the
# only color accent; diagrams can opt in to more via `classDef`.
_PALETTES = {
    "light": {
        "ink":   "#586e75",  # base01
        "paper": "#fdf6e3",  # base3
        "rule":  "#eee8d5",  # base2
        "muted": "#93a1a1",  # base1
    },
    "dark": {
        "ink":   "#93a1a1",  # base1
        "paper": "#002b36",  # base03
        "rule":  "#073642",  # base02
        "muted": "#586e75",  # base01
    },
}
_ACCENT = "#b58900"  # yellow, identical in both modes


def _theme_init(palette: dict[str, str]) -> str:
    ink, paper, rule, muted = palette["ink"], palette["paper"], palette["rule"], palette["muted"]
    variables = {
        "fontFamily": "Inter, system-ui, sans-serif",
        "fontSize": "17px",
        "primaryColor": rule, "primaryTextColor": ink, "primaryBorderColor": ink,
        "secondaryColor": paper, "secondaryTextColor": ink, "secondaryBorderColor": ink,
        "tertiaryColor": rule, "tertiaryTextColor": ink, "tertiaryBorderColor": ink,
        "lineColor": ink, "textColor": ink, "mainBkg": rule,
        "nodeBorder": ink, "defaultLinkColor": ink, "titleColor": ink,
        "edgeLabelBackground": paper,
        "clusterBkg": paper, "clusterBorder": muted,
        "actorBkg": rule, "actorBorder": ink, "actorTextColor": ink, "actorLineColor": muted,
        "signalColor": ink, "signalTextColor": ink,
        "labelBoxBkgColor": rule, "labelBoxBorderColor": ink, "labelTextColor": ink,
        "loopTextColor": ink,
        "noteBkgColor": paper, "noteTextColor": ink, "noteBorderColor": _ACCENT,
        "activationBkgColor": rule, "activationBorderColor": ink,
        "sequenceNumberColor": ink,
    }
    return f'%%{{init: {json.dumps({"theme": "base", "themeVariables": variables})}}}%%\n'


_VARIANTS = {name: _theme_init(palette) for name, palette in _PALETTES.items()}


def _fetch_svg(source: str) -> bytes:
    req = urllib.request.Request(
        KROKI_URL,
        data=source.encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "text/plain",
            "User-Agent": "astuscg-site-builder/1.0",
            "Accept": "image/svg+xml",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Kroki rejected diagram ({exc.code}): {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Kroki unreachable: {exc.reason}") from exc


def _ensure_svg(source: str) -> str:
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
    path = DIAGRAM_DIR / f"{digest}.svg"
    if not path.exists():
        DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_fetch_svg(source))
    return digest


def _render_pair(raw: str) -> dict[str, str]:
    sources = {variant: init + raw for variant, init in _VARIANTS.items()}
    with ThreadPoolExecutor(max_workers=len(sources)) as pool:
        return dict(zip(sources, pool.map(_ensure_svg, sources.values())))


def render_mermaid_blocks(text: str) -> str:
    def sub(match: re.Match) -> str:
        raw = match.group(1)
        alt_match = _ALT_RE.search(raw)
        alt = html.escape(alt_match.group(1) if alt_match else "Diagram", quote=True)
        hashes = _render_pair(raw)
        return (
            '\n\n<figure class="diagram">\n'
            f'  <img src="/static/img/diagrams/{hashes["light"]}.svg" alt="{alt}" class="diagram-light" loading="lazy">\n'
            f'  <img src="/static/img/diagrams/{hashes["dark"]}.svg" alt="{alt}" class="diagram-dark" loading="lazy">\n'
            "</figure>\n\n"
        )

    return _BLOCK_RE.sub(sub, text)


def reset_cache() -> None:
    if DIAGRAM_DIR.exists():
        for path in DIAGRAM_DIR.glob("*.svg"):
            path.unlink()

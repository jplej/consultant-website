import hashlib
import re
import urllib.request
from pathlib import Path

KROKI_URL = "https://kroki.io/mermaid/svg"
DIAGRAM_DIR = Path(__file__).parent / "static" / "img" / "diagrams"
_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
_ALT_RE = re.compile(r"^\s*%%\s*alt:\s*(.+?)\s*$", re.MULTILINE)


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
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


def render_mermaid_blocks(text: str) -> str:
    def sub(match: re.Match) -> str:
        source = match.group(1)
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
        path = DIAGRAM_DIR / f"{digest}.svg"
        if not path.exists():
            DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)
            path.write_bytes(_fetch_svg(source))
        alt_match = _ALT_RE.search(source)
        alt = alt_match.group(1) if alt_match else "Diagram"
        return f"![{alt}](/static/img/diagrams/{digest}.svg)"

    return _BLOCK_RE.sub(sub, text)

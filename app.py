from datetime import date, datetime, timezone
from itertools import groupby
from pathlib import Path

import frontmatter
from docutils.core import publish_parts
from flask import Flask, abort, render_template, Response
from myst_parser.parsers.docutils_ import Parser as MystParser

CONTENT = Path(__file__).parent / "content"
SITE_NAME = "Astus"
SITE_URL = "https://example.com"
AUTHOR_EMAIL = "jp@astuscg.com"

MYST_EXTENSIONS = [
    "colon_fence", "deflist", "fieldlist", "tasklist",
    "strikethrough", "attrs_inline", "attrs_block",
    "smartquotes", "replacements",
    "dollarmath", "amsmath", "substitution",
]

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def render_myst(text: str) -> str:
    parts = publish_parts(
        source=text,
        parser=MystParser(),
        writer_name="html5",
        settings_overrides={
            "embed_stylesheet": False,
            "doctitle_xform": False,
            "report_level": 5,
            "myst_enable_extensions": MYST_EXTENSIONS,
        },
    )
    return parts["html_body"]


def _coerce_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date()
    return None


def load_doc(path: Path):
    post = frontmatter.loads(path.read_text(encoding="utf-8"))
    html = render_myst(post.content)
    meta = dict(post.metadata)
    if "date" in meta:
        meta["date"] = _coerce_date(meta["date"])
    return {"meta": meta, "html": html, "slug": path.stem}


def load_collection(folder: str, sort_by_date: bool = False):
    root = CONTENT / folder
    if not root.exists():
        return []
    docs = [load_doc(p) for p in root.glob("*.myst")]
    if sort_by_date:
        docs.sort(key=lambda d: d["meta"].get("date") or date.min, reverse=True)
    else:
        docs.sort(key=lambda d: d["slug"])
    return docs


@app.route("/")
def index():
    essays = load_collection("essays", sort_by_date=True)
    grouped = [
        (year, list(items))
        for year, items in groupby(essays, key=lambda d: (d["meta"].get("date") or date.min).year)
    ]
    return render_template("index.html", grouped=grouped)


@app.route("/<slug>/")
def essay(slug):
    path = CONTENT / "essays" / f"{slug}.myst"
    if not path.exists():
        # fall through to pages
        path = CONTENT / "pages" / f"{slug}.myst"
        if not path.exists():
            abort(404)
        return render_template("page.html", doc=load_doc(path))
    doc = load_doc(path)
    related = [
        e for e in load_collection("essays", sort_by_date=True)
        if e["slug"] != slug
    ][:3]
    return render_template("essay.html", doc=doc, related=related)


@app.route("/work/")
def work_index():
    projects = load_collection("projects")
    order = {"active": 0, "shipped": 1, "archived": 2}
    projects.sort(key=lambda d: (order.get(d["meta"].get("status", "shipped"), 9), d["slug"]))
    return render_template("work_index.html", projects=projects)


@app.route("/work/<slug>/")
def project(slug):
    path = CONTENT / "projects" / f"{slug}.myst"
    if not path.exists():
        abort(404)
    return render_template("project.html", doc=load_doc(path))


@app.route("/feed.xml")
def feed():
    essays = load_collection("essays", sort_by_date=True)
    xml = render_template("feed.xml", essays=essays, site_name=SITE_NAME, site_url=SITE_URL, now=datetime.now(timezone.utc))
    return Response(xml, mimetype="application/xml")


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


@app.context_processor
def inject_globals():
    return {"site_name": SITE_NAME, "author_email": AUTHOR_EMAIL}


if __name__ == "__main__":
    app.run(debug=True)

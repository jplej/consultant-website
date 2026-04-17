from datetime import date, datetime, timezone
from itertools import groupby
from pathlib import Path

import frontmatter
from docutils.core import publish_parts
from flask import Flask, abort, render_template, request, Response, url_for
from flask import redirect as flask_redirect
from myst_parser.parsers.docutils_ import Parser as MystParser
from werkzeug.routing import BaseConverter

from i18n import DEFAULT_LANG, LANGS, STRINGS, other

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


class LangConverter(BaseConverter):
    regex = "|".join(LANGS)


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.url_map.converters["lang"] = LangConverter


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


def load_collection(lang: str, folder: str, sort_by_date: bool = False):
    root = CONTENT / lang / folder
    if not root.exists():
        return []
    docs = [load_doc(p) for p in root.glob("*.myst")]
    if sort_by_date:
        docs.sort(key=lambda d: d["meta"].get("date") or date.min, reverse=True)
    else:
        docs.sort(key=lambda d: d["slug"])
    return docs


@app.route("/")
def root():
    return flask_redirect(url_for("index", lang=DEFAULT_LANG))


@app.route("/<lang:lang>/")
def index(lang):
    essays = load_collection(lang, "essays", sort_by_date=True)
    grouped = [
        (year, list(items))
        for year, items in groupby(essays, key=lambda d: (d["meta"].get("date") or date.min).year)
    ]
    return render_template("index.html", grouped=grouped)


@app.route("/<lang:lang>/<slug>/")
def essay(lang, slug):
    path = CONTENT / lang / "essays" / f"{slug}.myst"
    if not path.exists():
        path = CONTENT / lang / "pages" / f"{slug}.myst"
        if not path.exists():
            abort(404)
        return render_template("page.html", doc=load_doc(path))
    doc = load_doc(path)
    related = [
        e for e in load_collection(lang, "essays", sort_by_date=True)
        if e["slug"] != slug
    ][:3]
    return render_template("essay.html", doc=doc, related=related)


@app.route("/<lang:lang>/work/")
def work_index(lang):
    projects = load_collection(lang, "projects")
    order = {"active": 0, "shipped": 1, "archived": 2}
    projects.sort(key=lambda d: (order.get(d["meta"].get("status", "shipped"), 9), d["slug"]))
    return render_template("work_index.html", projects=projects)


@app.route("/<lang:lang>/work/<slug>/")
def project(lang, slug):
    path = CONTENT / lang / "projects" / f"{slug}.myst"
    if not path.exists():
        abort(404)
    return render_template("project.html", doc=load_doc(path))


@app.route("/<lang:lang>/feed.xml")
def feed(lang):
    essays = load_collection(lang, "essays", sort_by_date=True)
    xml = render_template("feed.xml", essays=essays, site_name=SITE_NAME, site_url=SITE_URL, now=datetime.now(timezone.utc))
    return Response(xml, mimetype="application/xml")


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


@app.context_processor
def inject_globals():
    lang = (request.view_args or {}).get("lang", DEFAULT_LANG)
    return {
        "site_name": SITE_NAME,
        "author_email": AUTHOR_EMAIL,
        "lang": lang,
        "other_lang": other(lang),
        "t": STRINGS[lang],
    }


if __name__ == "__main__":
    app.run(debug=True)

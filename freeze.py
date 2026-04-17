from flask_frozen import Freezer

from app import CONTENT, app
from i18n import LANGS

app.config["FREEZER_DESTINATION"] = "build"
app.config["FREEZER_RELATIVE_URLS"] = False
app.config["FREEZER_REMOVE_EXTRA_FILES"] = True

freezer = Freezer(app)


@freezer.register_generator
def index():
    for lang in LANGS:
        yield {"lang": lang}


@freezer.register_generator
def essay():
    for lang in LANGS:
        for p in (CONTENT / lang / "essays").glob("*.myst"):
            yield {"lang": lang, "slug": p.stem}
        for p in (CONTENT / lang / "pages").glob("*.myst"):
            yield {"lang": lang, "slug": p.stem}


@freezer.register_generator
def project():
    for lang in LANGS:
        for p in (CONTENT / lang / "projects").glob("*.myst"):
            yield {"lang": lang, "slug": p.stem}


@freezer.register_generator
def feed():
    for lang in LANGS:
        yield {"lang": lang}


if __name__ == "__main__":
    freezer.freeze()

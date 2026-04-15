from flask_frozen import Freezer

from app import CONTENT, app

app.config["FREEZER_DESTINATION"] = "build"
app.config["FREEZER_RELATIVE_URLS"] = False
app.config["FREEZER_REMOVE_EXTRA_FILES"] = True

freezer = Freezer(app)


@freezer.register_generator
def essay():
    for p in (CONTENT / "essays").glob("*.myst"):
        yield {"slug": p.stem}
    # `essay` route also serves /pages/* by fallthrough
    for p in (CONTENT / "pages").glob("*.myst"):
        yield {"slug": p.stem}


@freezer.register_generator
def project():
    for p in (CONTENT / "projects").glob("*.myst"):
        yield {"slug": p.stem}


if __name__ == "__main__":
    freezer.freeze()

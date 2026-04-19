LANGS = ("en",)
DEFAULT_LANG = "en"

STRINGS = {
    "en": {
        "writing": "Writing",
        "work": "Work",
        "about": "About",
        "read_next": "Read next",
        "nothing_yet": "Nothing yet.",
        "not_found": "Not found.",
        "back_home": "Back home",
        "active": "active",
        "shipped": "shipped",
        "archived": "archived",
    },
    "fr": {
        "writing": "Écrits",
        "work": "Projets",
        "about": "À propos",
        "read_next": "Lire aussi",
        "nothing_yet": "Rien pour le moment.",
        "not_found": "Page introuvable.",
        "back_home": "Retour",
        "active": "actif",
        "shipped": "livré",
        "archived": "archivé",
    },
}


def other(lang: str) -> str:
    return "fr" if lang == "en" else "en"

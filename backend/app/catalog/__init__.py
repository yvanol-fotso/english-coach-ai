from app.catalog.languages import LANGUAGES
from app.catalog.scenarios import SCENARIOS
from app.catalog.tools import TOOLS
from app.catalog.topics import TOPICS
from app.catalog.units import UNITS

LANGUAGE_BY_ID = {lang.code: lang for lang in LANGUAGES}
SCENARIO_BY_ID = {s.id: s for s in SCENARIOS}
TOOL_BY_ID = {t.id: t for t in TOOLS}
UNIT_BY_ID = {u.id: u for u in UNITS}


def public() -> dict:
    return {
        "languages": [
            {"code": l.code, "native": l.native, "locale": l.locale, "label": l.label, "available": l.available}
            for l in LANGUAGES
        ],
        "topics": [{"id": t.id, "label": t.label, "starter": t.starter} for t in TOPICS],
        "scenarios": [{"id": s.id, "label": s.label, "starter": s.starter, "chip": s.chip} for s in SCENARIOS],
        "tools": [t.public() for t in TOOLS],
        "units": [{"id": u.id, "title": u.title, "goal": u.goal, "level": u.level} for u in UNITS],
    }

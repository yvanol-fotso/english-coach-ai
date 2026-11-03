from app.catalog.scenarios import SCENARIOS
from app.catalog.tools import TOOLS
from app.catalog.topics import TOPICS

SCENARIO_BY_ID = {s.id: s for s in SCENARIOS}
TOOL_BY_ID = {t.id: t for t in TOOLS}


def public() -> dict:
    return {
        "topics": [{"id": t.id, "label": t.label, "starter": t.starter} for t in TOPICS],
        "scenarios": [{"id": s.id, "label": s.label, "starter": s.starter, "chip": s.chip} for s in SCENARIOS],
        "tools": [t.public() for t in TOOLS],
    }

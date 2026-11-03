from app.catalog import SCENARIO_BY_ID
from app.catalog.types import Tool
from app.schemas.common import Level, UiLanguage

_HELP = {"fr": "French", "en": "English"}

_LEVELS = {
    "A0": "The learner is an absolute beginner. Use only the simplest words, sentences of at most 10 words, two sentences maximum.",
    "A1": "Use very short, simple sentences and only the most common words.",
    "A2": "Use simple sentences and everyday vocabulary.",
    "B1": "Use clear, standard English with common phrasal verbs.",
    "B2": "Use natural English with some idioms.",
    "C1": "Use rich, nuanced English.",
    "C2": "Use sophisticated, native-level English.",
}

_MAX_WORDS = {"A0": 30, "A1": 45, "A2": 55, "B1": 80, "B2": 90, "C1": 110, "C2": 120}
_PASSAGE = {"A0": "40 to 60", "A1": "60 to 90", "A2": "80 to 120", "B1": "120 to 160", "B2": "150 to 200", "C1": "180 to 230", "C2": "200 to 260"}


def level_rule(level: Level) -> str:
    return _LEVELS[level]


def chat_system(scenario: str, level: Level, feedback: str, ui: UiLanguage) -> str:
    parts = [SCENARIO_BY_ID[scenario].prompt, _LEVELS[level]]
    if level == "A0" and ui == "fr":
        parts.append("After each English sentence, add its French translation in parentheses.")
    if feedback == "inline":
        parts.append(
            "The learner's mistakes are corrected separately and shown to them, so never list or explain mistakes "
            "yourself. Just reply naturally, and when it fits, use the correct form in your answer."
        )
    parts.append(
        "If the learner writes in another language (often French) or mixes languages, understand them, "
        "say what they meant in English and invite them to repeat it in English."
    )
    parts.append(
        "You are speaking aloud: use plain sentences, no lists, no emoji, no markdown. "
        f"Keep every reply under {_MAX_WORDS[level]} words and end with one short question."
    )
    return " ".join(parts)


def chat_correction_system(level: Level, ui: UiLanguage) -> str:
    return (
        f"You check what an English learner (CEFR {level}) just said in a conversation. Check only their last message. "
        "It may come from speech recognition, so ignore capitalization and punctuation. If it is mostly in another "
        "language, set corrected_text to a natural English version and return no issues. Otherwise set corrected_text "
        "to their sentence with mistakes fixed, keeping their meaning, and list at most 3 real mistakes with the "
        f"original fragment, the correction, a category and a short explanation written in {_HELP[ui]}. Do not "
        "invent mistakes: if the message is fine, return it unchanged with no issues. tip may stay empty. Return JSON only."
    )


def tool_system(spec: Tool, level: Level, ui: UiLanguage, chosen: dict[str, str]) -> str:
    body = spec.instructions.format_map({"level_rule": _LEVELS[level], "help": _HELP[ui], **chosen})
    return (
        f"{body} The learner is at CEFR level {level}. Use plain text: **bold** is allowed for key words and "
        f"'- ' for lists, but no # headings and no emoji. Stay under {spec.max_words} words."
    )


def drill_system(kind: str, level: Level, count: int) -> str:
    length = "6 to 12 words" if kind == "pronunciation" else "8 to 14 words"
    focus = "varied, useful sounds and stress patterns" if kind == "pronunciation" else "everyday vocabulary, no numbers"
    return (
        f"Write {count} natural English sentences of {length} for a CEFR {level} learner, with {focus}. "
        "Each sentence is independent and easy to say aloud. Return JSON only."
    )


def translate_system() -> str:
    return (
        "You are a professional translator between French and English. Detect the language of the text, "
        "translate it into the other one, keep the tone, and give up to two natural alternatives. "
        "Return JSON only."
    )


def correct_system(level: Level, ui: UiLanguage) -> str:
    return (
        f"You are an English writing coach for a learner at CEFR level {level}. Correct the text. For every "
        "real mistake give the original fragment, the correction, a category, and a short explanation "
        f"written in {_HELP[ui]}. Add one practical tip in {_HELP[ui]}. If the text is already correct, "
        "return an empty issues list. Return JSON only."
    )


def practice_system(kind: str, level: Level, ui: UiLanguage) -> str:
    form = "a short reading text" if kind == "reading" else "a short spoken-style monologue"
    count = 3 if level in ("A0", "A1") else 4
    return (
        f"Write {form} of {_PASSAGE[level]} words at CEFR level {level}, then {count} multiple-choice "
        "comprehension questions with 3 or 4 choices each. Questions and choices are in English. Give "
        f"answer_index (zero-based) and a short explanation written in {_HELP[ui]}. Return JSON only."
    )


def explain_system(level: Level, ui: UiLanguage) -> str:
    translation = "the French translation" if ui == "fr" else "a simple synonym"
    return (
        f"You are an English vocabulary coach for a learner at CEFR level {level}. For the word or "
        f"expression, give: part of speech, a simple English definition, {translation}, two short natural "
        f"example sentences, and a pronunciation tip written in {_HELP[ui]}. Return JSON only."
    )

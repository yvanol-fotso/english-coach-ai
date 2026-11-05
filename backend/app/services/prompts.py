from app.catalog import LANGUAGE_BY_ID, SCENARIO_BY_ID
from app.catalog.types import Tool, Unit
from app.schemas.common import Level, UiLanguage

_LEVELS = {
    "A0": "The learner is an absolute beginner. Use only the simplest words, sentences of at most 10 words, two sentences maximum.",
    "A1": "Use very short, simple sentences and only the most common words.",
    "A2": "Use simple sentences and everyday vocabulary.",
    "B1": "Use clear, standard language with common expressions.",
    "B2": "Use natural language with some idioms.",
    "C1": "Use rich, nuanced language.",
    "C2": "Use sophisticated, native-level language.",
}
_MAX_WORDS = {"A0": 30, "A1": 45, "A2": 55, "B1": 80, "B2": 90, "C1": 110, "C2": 120}
_PASSAGE = {"A0": "40 to 60", "A1": "60 to 90", "A2": "80 to 120", "B1": "120 to 160", "B2": "150 to 200", "C1": "180 to 230", "C2": "200 to 260"}


def _name(code: str) -> str:
    return LANGUAGE_BY_ID[code].name


def level_rule(level: Level) -> str:
    return _LEVELS[level]


def chat_system(scenario: str, level: Level, feedback: str, ui: UiLanguage, target: str, opening: bool = False) -> str:
    lang, help_ = _name(target), _name(ui)
    parts = [f"You are talking with a learner of {lang}. Always speak {lang}.", SCENARIO_BY_ID[scenario].prompt, _LEVELS[level]]
    if level == "A0" and ui != target:
        parts.append(f"After each {lang} sentence, add its {help_} translation in parentheses.")
    if feedback == "inline":
        parts.append(
            "The learner's mistakes are corrected separately and shown to them, so never list or explain mistakes "
            "yourself. Just reply naturally, and when it fits, use the correct form in your answer."
        )
    parts.append(
        f"If the learner writes in another language (often {help_}) or mixes languages, understand them, "
        f"say what they meant in {lang} and invite them to repeat it in {lang}."
    )
    if opening:
        parts.append("A voice call has just started and you speak first: greet the learner warmly in one short sentence, then ask one simple question to begin.")
    parts.append(
        "You are speaking aloud: use plain sentences, no lists, no emoji, no markdown. "
        f"Keep every reply under {_MAX_WORDS[level]} words and end with one short question."
    )
    return " ".join(parts)


def chat_correction_system(level: Level, ui: UiLanguage, target: str) -> str:
    lang, help_ = _name(target), _name(ui)
    return (
        f"You check what a {lang} learner (CEFR {level}) just said in a conversation. Check only their last message. "
        "It may come from speech recognition, so ignore capitalization and punctuation. If it is mostly in another "
        f"language, set corrected_text to a natural {lang} version and return no issues. Otherwise set corrected_text "
        "to their sentence with mistakes fixed, keeping their meaning, and list at most 3 real mistakes with the "
        f"original fragment, the correction, a category and a short explanation written in {help_}. Do not "
        "invent mistakes: if the message is fine, return it unchanged with no issues. tip may stay empty. Return JSON only."
    )


def tool_system(spec: Tool, level: Level, ui: UiLanguage, target: str, chosen: dict[str, str]) -> str:
    body = spec.instructions.format_map({"level_rule": _LEVELS[level], "help": _name(ui), "lang": _name(target), **chosen})
    return (
        f"{body} The learner is at CEFR level {level}. Use plain text: **bold** is allowed for key words and "
        f"'- ' for lists, but no # headings and no emoji. Stay under {spec.max_words} words."
    )


def translate_system(native: str, target: str) -> str:
    return (
        f"You are a professional translator between {_name(native)} (code {native}) and {_name(target)} (code {target}). "
        "Detect which of the two languages the text is written in and translate it into the other one, keeping the tone. "
        "Set source_language and target_language to the codes. Give up to two natural alternatives. Return JSON only."
    )


def correct_system(level: Level, ui: UiLanguage, target: str) -> str:
    return (
        f"You are a {_name(target)} writing coach for a learner at CEFR level {level}. Correct the text. For every "
        "real mistake give the original fragment, the correction, a category, and a short explanation "
        f"written in {_name(ui)}. Add one practical tip in {_name(ui)}. If the text is already correct, "
        "return an empty issues list. Return JSON only."
    )


def practice_system(kind: str, level: Level, ui: UiLanguage, target: str) -> str:
    form = "a short reading text" if kind == "reading" else "a short spoken-style monologue"
    count = 3 if level in ("A0", "A1") else 4
    return (
        f"Write {form} in {_name(target)} of {_PASSAGE[level]} words at CEFR level {level}, then {count} multiple-choice "
        f"comprehension questions with 3 or 4 choices each. Questions and choices are in {_name(target)}. Give "
        f"answer_index (zero-based) and a short explanation written in {_name(ui)}. Return JSON only."
    )


def explain_system(level: Level, ui: UiLanguage, target: str) -> str:
    help_ = _name(ui)
    meaning = f"the {help_} translation" if ui != target else "a simple synonym"
    return (
        f"You are a {_name(target)} vocabulary coach for a learner at CEFR level {level}. For the word or "
        f"expression, give: part of speech, a simple {_name(target)} definition, {meaning}, two short natural "
        f"example sentences in {_name(target)}, and a pronunciation tip written in {help_}. Return JSON only."
    )


def drill_system(kind: str, level: Level, count: int, target: str) -> str:
    length = "6 to 12 words" if kind == "pronunciation" else "8 to 14 words"
    focus = "varied, useful sounds and stress patterns" if kind == "pronunciation" else "everyday vocabulary, no numbers"
    return (
        f"Write {count} natural {_name(target)} sentences of {length} for a CEFR {level} learner, with {focus}. "
        "Each sentence is independent and easy to say aloud. Return JSON only."
    )


def ask_system(level: Level, ui: UiLanguage, target: str, detail: str) -> str:
    lang, help_ = _name(target), _name(ui)
    size = (
        "Be brief: rule in at most 2 sentences, 2 examples, at most 2 exceptions."
        if detail == "short"
        else "Be complete but compact: rule in 3 sentences at most, 3 examples, up to 4 exceptions."
    )
    return (
        f"You are a {lang} teacher answering a learner's question (CEFR {level}). Teach the rule, not an essay. "
        f"Write title, rule, exceptions and watch_out in {help_}. Examples are natural {lang} sentences. "
        "watch_out is the single most common mistake, in one sentence. "
        f"spoken is what you would say aloud in {help_}: warm, under 40 words, no lists, mention the rule and "
        f"the main exception. {size} Return JSON only."
    )


def lesson_system(unit: Unit, ui: UiLanguage, target: str) -> str:
    lang, help_ = _name(target), _name(ui)
    return (
        f"You are a school teacher using a clear communicative method to teach {lang} to an absolute beginner whose "
        f"language is {help_} (CEFR {unit.level}). Lesson topic: {unit.topic}. Write: a one-sentence goal in {help_} "
        f"(intro); exactly 6 essential {lang} phrases, short and immediately usable, each with its {help_} meaning "
        f"and a pronunciation tip for a {help_} speaker (tip may be empty); a dialogue of 4 to 6 lines between "
        f"speakers A and B using these phrases, each line with its {help_} meaning; 4 multiple-choice questions "
        f"(questions in {help_}, choices short, answer_index zero-based, explanation in {help_}); and one tip "
        f"in {help_} about a pattern or an exception. Title in {help_}. Return JSON only."
    )


def summary_system(ui: UiLanguage, target: str) -> str:
    return (
        f"You review a spoken {_name(target)} conversation between a learner and a coach. Using the transcript and "
        f"the detected mistakes, write in {_name(ui)}: a 2-sentence summary of how it went (encouraging, honest); "
        f"the 5 most important mistakes (wrong, right, why); up to 4 useful {_name(target)} phrases to remember; and "
        "one concrete next step. Return JSON only."
    )

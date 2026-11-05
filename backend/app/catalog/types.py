from dataclasses import dataclass

Text = dict[str, str]


def T(fr: str, en: str) -> Text:
    return {"fr": fr, "en": en}


def S(en: str, fr: str, es: str) -> dict[str, str]:
    """A first line in each learnable language. Missing languages fall back to English in the app."""
    return {"en": en, "fr": fr, "es": es}


@dataclass(frozen=True)
class Language:
    code: str
    name: str  # English name, used inside prompts
    native: str
    locale: str  # BCP-47 tag for speech recognition and voices
    label: Text
    available: bool = True


@dataclass(frozen=True)
class Unit:
    id: str
    title: Text
    goal: Text
    topic: str  # what the lesson teaches, in plain English for the model
    level: str = "A0"


@dataclass(frozen=True)
class Scenario:
    id: str
    label: Text
    prompt: str
    starter: dict[str, str]
    chip: bool = True


@dataclass(frozen=True)
class Topic:
    id: str
    label: Text
    starter: dict[str, str]


@dataclass(frozen=True)
class Choice:
    id: str
    label: Text


@dataclass(frozen=True)
class Option:
    id: str
    label: Text
    choices: tuple[Choice, ...]


@dataclass(frozen=True)
class Tool:
    id: str
    icon: str
    skill: str
    title: Text
    description: Text
    placeholder: Text
    instructions: str
    options: tuple[Option, ...] = ()
    temperature: float = 0.7
    max_words: int = 250

    def public(self) -> dict:
        return {
            "id": self.id,
            "icon": self.icon,
            "skill": self.skill,
            "title": self.title,
            "description": self.description,
            "placeholder": self.placeholder,
            "options": [
                {"id": o.id, "label": o.label, "choices": [{"id": c.id, "label": c.label} for c in o.choices]}
                for o in self.options
            ],
        }


def option(option_id: str, label: Text, *choices: tuple[str, Text]) -> Option:
    return Option(option_id, label, tuple(Choice(cid, clabel) for cid, clabel in choices))

from dataclasses import dataclass

Text = dict[str, str]


def T(fr: str, en: str) -> Text:
    return {"fr": fr, "en": en}


@dataclass(frozen=True)
class Scenario:
    id: str
    label: Text
    prompt: str
    starter: str = ""
    chip: bool = True


@dataclass(frozen=True)
class Topic:
    id: str
    label: Text
    starter: str


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

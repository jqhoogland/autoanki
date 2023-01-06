import enum
from dataclasses import dataclass, field
from typing import Dict, List, TypedDict


class NoteType(enum.Enum):
    BASIC = "Basic"
    CLOZE = "Cloze"
    BASIC_AND_REVERSE = "Basic (and reversed card)"


@dataclass
class Settings:
    note_type: NoteType
    deck: str
    api_key: str

@dataclass
class Note:
    type: NoteType
    fields: Dict[str, str]
    tags: List[str] = field(default_factory=list)


import enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, TypedDict


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
    # Field name: Field value
    # Basic: Front, Back
    # Cloze: Text
    # Basic (and reversed card): Front, Back
    fields: Dict[str, str]
    tags: List[str] = field(default_factory=list)

    @classmethod
    def create_basic(cls, front: str, back: str, tags: Optional[List[str]] = None) -> "Note":
        return cls(
            type=NoteType.BASIC,
            fields={
                "Front": front,
                "Back": back,
            },
            tags=tags or [],
        )

    @classmethod
    def create_cloze(cls, text: str, tags: Optional[List[str]] = None) -> "Note":
        return cls(
            type=NoteType.CLOZE,
            fields={
                "Text": text,
            },
            tags=tags or [],
        )

    @classmethod
    def create_basic_and_reverse(cls, front: str, back: str, tags: Optional[List[str]] = None) -> "Note":
        return cls(
            type=NoteType.BASIC_AND_REVERSE,
            fields={
                "Front": front,
                "Back": back,
            },
            tags=tags or [],
        )
        
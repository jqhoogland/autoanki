
from typing import List
from autoanki.types_ import Note, NoteType


def create_notes(text: str, note_type: NoteType, api_key: str) -> List[Note]:
    return [
        Note.create_basic("Question 2", "Answer 2"),
        Note.create_basic_and_reverse("Question 3", "Answer 3"),
        Note.create_cloze("Question 4 {{c1::Answer 4}}"),
    ]

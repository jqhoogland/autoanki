"""
Contains the shell script to run from the command line.
"""

from pathlib import Path
from typing import List

from autoanki.create_notes import create_notes
from autoanki.types_ import Note, NoteType, Settings
from autoanki.upload_notes import upload_notes


def notes_to_csv(notes: List[NoteType], note_type: NoteType):
    """
    Writes the notes to a CSV file.
    """
    with open("notes.csv", "w") as notes_file:
        if note_type == NoteType.BASIC or note_type == NoteType.BASIC_AND_REVERSE:
            notes_file.write("Front,Back,Tags")
            for note in notes:
                notes_file.write(f"{note.fields['Front']},{note.fields['Back']},{','.join(note.tags)}")
        elif note_type == NoteType.CLOZE:
            notes_file.write("Text,Tags")
            for note in notes: 
                notes_file.write(f"{note.fields['Text']},{','.join(note.tags)}")


def notes_from_csv(file: Path, note_type: NoteType) -> List[Note]:
    """
    Reads the notes from a CSV file.
    """
    notes = []
    
    with open(file, "r") as notes_file:
        if note_type == NoteType.BASIC or note_type == NoteType.BASIC_AND_REVERSE:
            for line in notes_file.readlines()[1:]:
                front, back, tags = line.split(",")
                notes.append(Note(
                    type=note_type,
                    fields={
                        "Front": front,
                        "Back": back,
                    },
                    tags=tags.split(","),
                ))
        elif note_type == NoteType.CLOZE:
            for line in notes_file.readlines()[1:]:
                text, tags = line.split(",")
                notes.append(Note(
                    type=note_type,
                    fields={
                        "Text": text,
                    },
                    tags=tags.split(","),
                ))

    return notes

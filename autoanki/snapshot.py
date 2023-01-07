"""
Contains the shell script to run from the command line.
"""

import csv
from pathlib import Path
from typing import List

from autoanki.types_ import Note, NoteType, Settings


def notes_to_csv(notes: List[Note], note_type: NoteType):
    """
    Writes the notes to a CSV file.
    """
    csv.QUOTE_ALL = True

    with open("notes.csv", "w") as notes_file:
        writer = csv.writer(notes_file)
        
        if note_type == NoteType.BASIC or note_type == NoteType.BASIC_AND_REVERSE:
            writer.writerow(["Front", "Back", "Tags"])
            for note in notes:
                writer.writerow([note.fields["Front"], note.fields["Back"], ",".join(note.tags)])
        
        elif note_type == NoteType.CLOZE:
            writer.writerow(["Text", "Tags"])   
            for note in notes: 
                writer.writerow([note.fields["Text"], ",".join(note.tags)])


def notes_from_csv(file: Path, note_type: NoteType) -> List[Note]:
    """
    Reads the notes from a CSV file.
    """
    notes = []
    
    with open(file, "r") as notes_file:
        reader = csv.reader(notes_file)
        next(reader)

        if note_type == NoteType.BASIC or note_type == NoteType.BASIC_AND_REVERSE:
            for line in reader:
                front, back, tags = line
                notes.append(Note(
                    type=note_type,
                    fields={
                        "Front": front,
                        "Back": back,
                    },
                    tags=tags.split(","),
                ))
                
        elif note_type == NoteType.CLOZE:
            for line in reader:
                text, tags = line
                notes.append(Note(
                    type=note_type,
                    fields={
                        "Text": text,
                    },
                    tags=tags.split(","),
                ))

    return notes

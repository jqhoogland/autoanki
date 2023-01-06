"""
Contains the shell script to run from the command line.
"""

import dataclasses
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, TypedDict

import typer
import yaml

from autoanki.snapshot import notes_from_csv, notes_to_csv
from autoanki.types_ import Note, NoteType, Settings

# from autoanki.create_notes import create_notes
# from autoanki.upload_notes import upload_notes

def create_notes(*args, **kwargs):
    raise NotImplementedError

def upload_notes(*args, **kwargs):
    raise NotImplementedError

def load_settings(note_type: NoteType, deck: str, api_key: Optional[str] = None) -> Settings:
    """
    Loads the settings from the settings file.
    """
    with open("settings.yaml") as settings_file:
        settings = yaml.safe_load(settings_file)
        
    if api_key is None:
        api_key = typer.prompt("Please enter your AnkiConnect API Key")

    settings.update({
        "note_type": note_type,
        "deck": deck,
        "api_key": api_key,
    })

    with open("settings.yaml", "w") as settings_file:
        yaml.dump(settings, settings_file)

    return Settings(**settings)


def main(file: Path, note_type: NoteType = NoteType.BASIC, deck: str = "Default", api_key: Optional[str] = None):
    """
    TODO: Verbose option to print out each question/answer pair one at a time for feedback.
    """
    settings = load_settings(note_type, deck, api_key)
    data = file.read_text()

    # Use the OpenAI API to create the notes
    notes = create_notes(data, note_type=settings.note_type, api_key=settings.api_key)
    
    # Give the user a chance to edit the notes before we upload them
    notes_to_csv(notes, note_type=settings.note_type)
    typer.prompt("Press enter to upload to Anki")
    notes = notes_from_csv(Path("notes.csv"), note_type=settings.note_type)
    
    # Use AnkiConnect to upload the notes
    upload_notes(notes, note_type=settings.note_type, deck=settings.deck)


if __name__ == "__main__":
    typer.run(main)

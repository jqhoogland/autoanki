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
from autoanki.create_notes import create_notes
from autoanki.upload_notes import upload_notes


def load_settings(note_type: NoteType, deck: str, api_key: Optional[str] = None) -> Settings:
    """
    Loads the settings from the settings file.
    """
    with open("settings.yaml") as settings_file:
        settings = yaml.safe_load(settings_file)

    api_key = api_key or settings.get("api_key")
        
    if api_key is None:
        api_key = typer.prompt("Please enter your OpenAI API Key")

    settings.update({
        "note_type": note_type.value,
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
    text = file.read_text()

    # Use the OpenAI API to create the notes
    notes = create_notes(text, note_type=settings.note_type, api_key=settings.api_key)
    
    # Give the user a chance to edit the notes before we upload them
    notes_to_csv(notes, note_type=settings.note_type)
    should_upload = typer.prompt("Upload to Anki (y/n)?")

    if should_upload.lower() != "y":
        return

    # notes = notes_from_csv(Path("notes.csv"), note_type=settings.note_type)
    
    # Use AnkiConnect to upload the notes
    upload_notes(notes, deck=settings.deck)


if __name__ == "__main__":
    typer.run(main)

"""
Contains the shell script to run from the command line.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Generator, List, Optional, TypedDict

import typer
import yaml

from autoanki.create_notes import create_notes
from autoanki.scrape import get_text
from autoanki.snapshot import notes_from_csv, notes_to_csv
from autoanki.types_ import Note, NoteType, Settings
from autoanki.upload_notes import upload_notes


def load_settings(note_type: NoteType, deck: str, api_key: Optional[str] = None) -> Settings:
    """
    Loads the settings from the settings file.
    """
    try: 
        with open("settings.yaml") as settings_file:
            settings = yaml.safe_load(settings_file)
    except FileNotFoundError:
        settings = {}

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


PathOrURL = typer.Argument(..., help="Path to a file or URL to a webpage to create notes from")


def prompt_note(note: Note) -> Note:
    return Note(
        type=note.type,
        fields={
            k: typer.prompt(k, default=v)
            for k, v in note.fields.items()
        },
        tags=typer.prompt("Tags", default="").split(","),
    )


def filter_and_edit_notes(notes: List[Note], interactive: bool) -> Generator[Note, None, None]:
    for note in notes:
        print("\n")
        print(str(note))

        if interactive:
            should_add = typer.prompt("Do you want to add or edit this note? (y/n/e)", default="y")
            
            if should_add.lower() == "y":
                yield note
            elif should_add.lower() == "e":
                yield prompt_note(note)

        else:
            yield note
 
def main(
    file: str = PathOrURL, 
    note_type: NoteType = NoteType.BASIC, 
    deck: str = "Default", 
    api_key: Optional[str] = None,
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Whether to run the script interactively")
):
    """
    Creates notes from a file or URL with the OpenAI API and uploads them to Anki. 
    """
    settings = load_settings(note_type, deck, api_key)
    text = get_text(file)

    # Use the OpenAI API to create the notes
    suggested_notes = create_notes(text, note_type=settings.note_type, api_key=settings.api_key)
    notes = list(filter_and_edit_notes(suggested_notes, interactive))

    # Give the user a chance to edit the notes before we upload them
    notes_to_csv(notes, note_type=settings.note_type)
    should_upload = typer.prompt(
        "\n" + "-" * 80 + "\n" + "Do you want to upload these notes to Anki? (y/n)\n" +
        "[You can edit the notes in notes.csv before uploading.]",
        default="y"
    )

    if should_upload.lower() != "y":
        return

    notes = notes_from_csv(Path("notes.csv"), note_type=settings.note_type)
    
    # Use AnkiConnect to upload the notes
    upload_notes(notes, deck=settings.deck)


if __name__ == "__main__":
    typer.run(main)

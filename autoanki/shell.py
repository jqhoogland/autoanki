"""
Contains the shell script to run from the command line.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, TypedDict

import requests
# import textract
import typer
import yaml

from autoanki.create_notes import create_notes
from autoanki.pdf_scrape import scrape_text_from_arxiv, scrape_text_from_file
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


def get_text(file: str) -> str:
    """
    Gets the text from the file or URL.
    """
    if "arxiv.org" in file:
        if not file.endswith(".pdf"):
            file = file.replace("abs", "pdf")
            file += ".pdf"

        print(file)
        return scrape_text_from_arxiv(file)

    if file.startswith("http"):
        response = requests.get(file)
        # filetype = response.headers["Content-Type"]
        # filepath = Path(f"../data/{file.split('/')[-1]}")
        # filepath.write_bytes(response.content)
        return response.text
    
    filepath = Path(file)
    
    # PDFs are a special case
    if str(filepath).endswith(".pdf"):
        return scrape_text_from_file(filepath)
    
    # return textract.process(file)
    return filepath.read_text()


def main(file: str = PathOrURL, note_type: NoteType = NoteType.BASIC, deck: str = "Default", api_key: Optional[str] = None):
    """
    TODO: Verbose option to print out each question/answer pair one at a time for feedback.
    """
    settings = load_settings(note_type, deck, api_key)
    text = get_text(file)

    # Use the OpenAI API to create the notes
    notes = create_notes(text, note_type=settings.note_type, api_key=settings.api_key)
    
    # Show the user the notes we created
    for note in notes:
        print(str(note))

    # Give the user a chance to edit the notes before we upload them
    notes_to_csv(notes, note_type=settings.note_type)
    should_upload = typer.prompt("Upload to Anki (y/n)?")

    if should_upload.lower() != "y":
        return

    notes = notes_from_csv(Path("notes.csv"), note_type=settings.note_type)
    
    # Use AnkiConnect to upload the notes
    upload_notes(notes, deck=settings.deck)


if __name__ == "__main__":
    typer.run(main)

import glob
import os
import urllib.request
from pathlib import Path
from typing import Union

import textract


def scrape_text_from_arxiv(link: str):
    file = Path("data") / link.split("/")[-1]

    if not file.exists():
        with urllib.request.urlopen(link) as web_file:
            file.write_bytes(web_file.read())

    return file


def get_text(file: Union[str, Path]) -> str:
    """
    Gets the text from the file or URL.
    """
    file = str(file)

    if "arxiv.org" in file:
        if not file.endswith(".pdf"):
            file = file.replace("abs", "pdf")
            file += ".pdf"

        file = scrape_text_from_arxiv(file)

    elif file.startswith("http"):
        response = urllib.request.urlopen(file)
        return response.text

    return str(textract.process(file))
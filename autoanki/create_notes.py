from typing import List

from autoanki.types_ import Note, NoteType
import openai

ELICIT_ANKI_MAP = {'Basic': 'Summarise this as a set of Anki flashcards.\n\n1) Q:',
                   'Basic (and reversed card)': 'Summarise this as a set of Anki flashcards.\n\n1) Q:',
                   'Cloze': 'Summarise and rewrite these notes as a set of fill in the blank flashcards.\n\n 1)'}


def create_notes(text: str, note_type: NoteType, api_key: str) -> List[Note]:
    """Takes in notes (text), an api_key, and a note_type (basic, cloze, basic-reversed)
    Uses GPT-3 to return a set of question answer pairs to be turned into Anki cards."""
    openai.api_key = api_key

    elicit_anki = ELICIT_ANKI_MAP['note_type']
    prompt = f'BEGIN NOTES\n\n{text}\n\nEND NOTES\n\n{elicit_anki}'
    answer = openai.Completion.create(model='text-davinci-003', prompt=prompt, max_tokens=512, temperature=0.7)
    answer_text = answer["choices"][0]["text"]
    cards = answer_text.splitlines()
    skip = 2 if note_type == "Cloze" else 5  # 1) vs. 1) Q:
    cards = [card[skip:] for card in cards]
    anki_cards = []
    for i in range(0, len(cards), 2):
        if note_type == "Cloze":
            underscore_index = cards[i].index('_')
            answer = "{{c1::" + cards[i + 1] + '}}'
            text = cards[i][:underscore_index] + answer + cards[underscore_index + 1:]
            anki_cards.append(Note.create_cloze(text))
        if note_type == "Basic":
            anki_cards.append(Note.create_basic(cards[i], cards[i + 1]))
        if note_type == "Basic (and reversed card)":
            anki_cards.append(Note.create_basic_and_reverse(cards[i], cards[i + 1]))
    return anki_cards

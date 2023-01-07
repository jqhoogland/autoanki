import re
from typing import List, Tuple

import openai
import transformers
import warnings

from autoanki.types_ import Note, NoteType

ELICIT_ANKI_MAP = {
    'Basic': 'Summarise this as a set of Anki flashcards.'
            '\n\n1) Q: What is the capital of Australia? A: Canberra.'
            '\n\n2) Q:',
    'Basic (and reversed card)': 'Summarise this as a set of Anki flashcards.'
                                '\n\n1) Q: What is the capital of Australia? A: Canberra is the capital of what country?'
                                '\n\n2) Q:',
    'Cloze': 'Summarise and rewrite these notes as a set of fill in the blank flashcards.'
            '\n\n1) Q: The capital of Australia is __________. A: Canberra'
            '\n\n2) Q:'
}


def read_qa_pair(text: str) -> Tuple[str, str]:
    """Splits a question of the kind "Q: ... A: ..." into a question and answer pair."""
    
    try:
        # Split the text into question and answer
        question, answer = text.split("A:")

        # Remove the "Q:" from the question
        question = question[3:].strip()

        # Remove the leading space from the answer
        answer = answer[1:].strip()

        return question, answer
    except:
        warnings.warn(f"Failed on: {text}")
        open("failed.txt", "a").write(text+"\n")
        return "", ""
    

def _create_notes(text: str, note_type: NoteType, api_key: str) -> List[Note]:
    """Takes in notes (text), an api_key, and a note_type (basic, cloze, basic-reversed)
    Uses GPT-3 to return a set of question answer pairs to be turned into Anki cards."""
    elicit_anki = ELICIT_ANKI_MAP[note_type]
    prompt = f'BEGIN NOTES\n\n{text}\n\nEND NOTES\n\n{elicit_anki}'

    answer = openai.Completion.create(model='text-davinci-003', prompt=prompt, max_tokens=512, temperature=0.7)
    answer_text = "2) Q: " + answer["choices"][0]["text"]
    
    pattern = r"\b\d+\)"
    note_texts = re.split(pattern, answer_text)[1:]

    # Split the note_texts into question and answer pairs
    qa_pairs = [
        read_qa_pair(note_text) for note_text in note_texts
    ]

    anki_cards = []

    for qa_pair in qa_pairs:
        q, a = qa_pair
        
        if note_type == "Cloze":
            underscore_index = q.index('_')
            answer = "{{c1::" + a + '}}'
            text = q[:underscore_index] + answer + q[underscore_index + 1:]
            anki_cards.append(Note.create_cloze(text))

        elif note_type == "Basic":
            anki_cards.append(Note.create_basic(q, a))

        elif note_type == "Basic (and reversed card)":
            anki_cards.append(Note.create_basic_and_reverse(q, a))

    return anki_cards


def create_notes(text: str, note_type: NoteType, api_key: str) -> List[Note]:
    """Wrapper to make sure we can fit our text into GPT-3'ss 4097 token limit."""
    openai.api_key = api_key

    config = transformers.GPT2Config(n_positions=9999999)
    tokenizer = transformers.GPT2Tokenizer.from_pretrained('gpt2', config=config)
    tokens = tokenizer.encode(text)

    # Break into chunks of 2048 tokens
    token_groups = [tokens[i:i+2048] for i in range(0, len(tokens), 2048)]

    # Decode the chunks
    chunks = [tokenizer.decode(token_group) for token_group in token_groups]

    return [
        note 
        for chunk in chunks 
        for note in _create_notes(chunk, note_type, api_key)
    ]
    # return _create_notes(text, note_type, api_key)




    
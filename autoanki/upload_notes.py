import json
import urllib.request

from types_ import Note


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


class AnkiConnectDeck:

    def __init__(self, name):
        self.name: str = name
        self.notes: list[Note] = []

    def parse(self, note: Note):
        return {
            'deckName': self.name,
            'modelName': note.type,
            'fields': note.fields,
            'options': {
                'allowDuplicate': False
            },
            'tags': note.tags
        }

    def send(self):
        invoke('createDeck', deck=self.name)
        invoke('addNotes', notes=[self.parse(note) for note in self.notes])

    def add_note(self, note):
        self.notes.append(note)

    def add_notes(self, notes):
        self.notes.extend(notes)


def upload_notes(notes: list[Note], deck: str):
    d = AnkiConnectDeck(deck)
    d.add_notes(notes)
    d.send()
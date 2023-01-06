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

    def __init__(self, deckname):
        self.deckname: str = deckname
        self.cards: list[Note] = []

    def parse(self, card: Note):
        return {
            'deckName': self.deckname,
            'modelName': card.type,
            'fields': card.fields,
            'options': {
                'allowDuplicate': False
            },
            'tags': card.tags
        }

    def send(self):
        invoke('createDeck', deck=self.deckname)
        invoke('addNotes', notes=[self.parse(card) for card in self.cards])

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        self.cards.extend(cards)

# sampleNotes = [
#     Note(
#         type='Basic',
#         fields={
#             'Front': 'foo',
#             'Back': 'bar'
#         },
#         tags=[
#             'tag1',
#             'tag2'
#         ]
#     ),
#     Note(
#         type='Basic',
#         fields={
#             'Front': 'foo2',
#             'Back': 'bar2'
#         },
#         tags=[
#             'tag1',
#             'tag2'
#         ]
#     )
# ]

# deckname = 'testdeck'
# deck = AnkiConnectDeck(deckname)
# deck.add_cards(sampleNotes)
# deck.send()

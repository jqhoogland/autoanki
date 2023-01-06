import json
import urllib.request

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


invoke('createDeck', deck='test1')

# add dummy cards to deck
invoke('addNote', note={
    'deckName': 'test1',
    'modelName': 'Basic',
    'fields': {
        'Front': 'foo',
        'Back': 'bar'
    },
    'options': {
        'allowDuplicate': False
    },
    'tags': [
        'tag1',
        'tag2'
    ]
})

deckname = 'test1'

class AnkiConnectDeck:

    def __init__(self, deckname):
        self.deckname = deckname

    def add_csv_row(self, row):
        front = row['front']
        back = row['back']
        if row['type'] == 'basic':
            note = self.basic(front, back)
        elif row['type'] == 'cloze':
            note = self.cloze(front)
        elif row['type'] == 'basic+reversed':
            note = self.create_basic_and_reversed(front, back)
        else:
            raise Exception('unknown type: {}'.format(row['type']))
        invoke('addNote', note=note)

    def basic(self, front: str, back: str):
        return {
            'deckName': deckname,
            'modelName': 'Basic',
            'fields': {
                'Front': front,
                'Back': back
            },
            'options': {
                'allowDuplicate': False
            }
        }

    def cloze(self, text: str):
        return {
            'deckName': deckname,
            'modelName': 'Cloze',
            'fields': {
                'Text': text
            },
            'options': {
                'allowDuplicate': False
            }
        }

    def create_basic_and_reversed(self, front: str, back: str): # replace with basic+reversed type
        return {
            'deckName': deckname,
            'modelName': 'Basic (and reversed card)',
            'fields': {
                'Front': front,
                'Back': back
            },
            'options': {
                'allowDuplicate': False
            }
        }



def process_csv(csv):
    deckname = 'test1'
    deck = AnkiConnectDeck(deckname)
    for row in csv:
        AnkiConnectDeck.add_csv_row(row)

result = invoke('deckNames')
print('got list of decks: {}'.format(result))
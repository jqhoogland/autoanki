# Autoanki

Automatically create Anki cards from text using language models


```
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

```
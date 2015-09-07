__author__ = 'fritz'
from pubsub.database.utils import is_remote_deck, get_remote_deck_id, get_note_ids_for_deck_id
from aqt import mw
import json
from copy import deepcopy

class Deck():
    def __init__(self, name, description, remote_id=None, local_id=None):
        self.name = name
        self.description = description
        self.remote_id = remote_id
        self.local_id = local_id
        # TODO if no local id create deck or load it

    @classmethod
    def from_anki(cls, local_id):
        if is_remote_deck(local_id):
            remote_id = get_remote_deck_id(local_id)
        else:
            remote_id = None
        anki_deck = mw.col.decks.get(local_id)
        name = anki_deck.get('name')
        description = anki_deck.get('desc')
        return cls(name, description, remote_id, local_id)

    def get_all_note_ids(self):
        return get_note_ids_for_deck_id(self.local_id)

    def json(self):
        deck_json = deepcopy(self)
        deck_json.__dict__.pop('local_id', None)
        deck_json = json.dumps(deck_json.__dict__)


        print(deck_json)
        return deck_json

__author__ = 'fritz'
from pubsub.database.utils import is_remote_deck, get_remote_deck_id, get_note_ids_for_deck_id
from aqt import mw
import json
from copy import deepcopy
from pubsub.database.models import db, AnkiPubSubDeck, AnkiPubSubDeck2AnkiDeck
from datetime import datetime


class Deck():
    def __init__(self, name, description, remote_id=None, local_id=None):
        self.name = name
        self.description = description
        self.author = None

        if local_id:
            db.connect()
            try:
                deck2anki = AnkiPubSubDeck2AnkiDeck.get(AnkiPubSubDeck2AnkiDeck.local_id == local_id)
                remote_id = deck2anki.remote_deck.uuid
            except AnkiPubSubDeck2AnkiDeck.DoesNotExist:
                pass
            db.close()
        if remote_id:
            db.connect()
            deck = AnkiPubSubDeck.get(AnkiPubSubDeck.uuid == remote_id)
            self.author = deck.author
            self.creation_date = deck.creation_date
            self.last_updated = deck.last_updated
            db.close()
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
        return deck_json

    def save(self):
        db.connect()
        deck, created = AnkiPubSubDeck.get_or_create(uuid=self.remote_id)
        if created:
            deck.creation_date = datetime.now()
            deck.author = self.author
            AnkiPubSubDeck2AnkiDeck.create_or_get(remote_deck=deck, local_id=self.local_id)
        deck.last_updated = datetime.now()
        deck.save()
        db.close()


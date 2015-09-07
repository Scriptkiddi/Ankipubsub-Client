__author__ = 'fritz'
from .models.Deck import Deck
from .models.Note import Note
from .models.Model import Model
from .models.Settings import DeckSettings
import requests


def sync_with_local_deck_id(local_id):
    anki_deck = Deck.from_anki(local_id)

    model_objects = {}
    notes = []
    for note_id in anki_deck.get_all_note_ids():
        note = Note.from_anki(note_id)
        if model_objects.get(note.model_id):
            model = model_objects.get(note.model_id)
        else:
            model = Model.from_anki(note.model_id)
            model.deck = anki_deck
            model_objects.update({note.model_id: model})
        note.deck = anki_deck
        note.model = model
        notes.append(note)

    # From this point on everything should have the correct relations to each other
    # now we start to sync with the server

    if anki_deck.remote_id:
        pass # TODO see if somethign changed
    else:
        deck_json = anki_deck.json()
        settings = DeckSettings(anki_deck.local_id)
        r = requests.post(settings.server_url+"decks/", data=deck_json, headers={"content-type": "application/json"})
        if r.status_code == requests.codes.ok:
            r = r.json()
            anki_deck.remote_id = r.get('id')
            print(anki_deck.remote_id)
            # todo save remote id /
            # todo maybe write __eq__ for the deck class to easily compare if there where any changes



        pass # TODO create deck on server
    for model in model_objects.values():
        if not model.remote_id:
            pass # create model on the server
        else:
            pass
            # TODO see if something changed
    for note in notes:
        if not note.remote_id:
            pass # todo create on server
        else:
            pass # todo check if something has changed
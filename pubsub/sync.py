__author__ = 'fritz'
from pubsub.models.Deck import Deck
from .models.Note import Note
from .models.Model import Model
from .models.Settings import DeckSettings
from connection.utils import create_on_server
from database.models import db



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
    settings = DeckSettings(anki_deck.local_id)
    print(anki_deck.remote_id)
    if anki_deck.remote_id:
        print("-----------------")
        # TODO see if somethign changed
        # todo maybe write __eq__ for the deck class to easily compare if there where any changes
    else:
        anki_deck.remote_id = create_on_server(anki_deck, settings)
        anki_deck.save()
        # todo save remote id /
    for model in model_objects.values():
        if model.remote_id:
            pass # TODO see if something changed
        else:
            for field in model.fields:
                print(field.remote_id)
                if not field.remote_id:
                    field.remote_id = create_on_server(field, settings)
                    field.save()
            for template in model.templates:
                print(template.remote_id)
                if not template.remote_id:
                    template.remote_id = create_on_server(template, settings)
                    template.save()
            model.remote_id = create_on_server(model, settings)
            #model.save()
    for note in notes:
        if note.remote_id:
            pass  # todo check if something has changed
        else:
            note.remote_id = create_on_server(note, settings)
            #note.save()

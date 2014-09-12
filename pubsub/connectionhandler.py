# !/usr/bin/python
#  -*- coding: utf-8 -*-
""" connectionhandler.py contains the connectionHandler class."""
import requests
import json
from Deck import AnkipubSubDeck
from Note import AnkipubSubNote
from Model import AnkipubSubModel
from copy import deepcopy


class connectionHandler(object):

    """
    Wrapper Class for server Connection.

    This class handels Session managment and the the calls to the server.
    """

    def __init__(self, serverUrl, username, password):
        """Build an object with a session and the passed login credentials."""
        self.url = serverUrl
        self.password = password
        self.username = username
        self.session = requests.Session()

    def push_deck(self, deck):
        """
        Push the passed deck to the server.

        Take the passed deck transform the models and notes to clean python
        dictionarys, because as an object they are a UserDict which
        can not be converted to json easily
        """
        deck = deepcopy(deck)
        self.login()  # Führe login durch

        notes = deck.get('notes')
        models = deck.get('models')

        for note in notes:
            notes[notes.index(note)] = note.data
        for model in models:
            models[models.index(model)] = model.data
        deck.update({'notes': notes, 'models': models})
        deck.setLastChange(str(deck.getLastChange()))

        # payload für die post request
        payload = deck.data

        # Content Header damit der Server weiß was kommt
        headers = {'content-type':  'application/json'}
        """wenn das deck schon eine ID hat dann wird an diese ID geschickt\
         wenn nicht an den normalen Handler"""
        if deck.getRemoteID():
            url = self.url+"/push/deck/"+deck.getRemoteID()
        else:
            url = self.url+"/push/deck"

        # Führe Post aus
        payload
        deckResponse = self.session.post(url,
                                         data=json.dumps(payload),
                                         headers=headers).json()

        deck = AnkipubSubDeck.fromJsonObject(deckResponse)

        self.logout()
        newNotes = []
        newModels = []
        for note in deck.getNotes():
            newNotes.append(AnkipubSubNote(note))
        deck.update({'notes': newNotes})
        for model in deck.get('models'):
            newModels.append(AnkipubSubModel(model))
        deck.update({'models': newModels})
        return deck

    def pull_deck(self, deckid, **kwargs):
        """
        Pull the deck with the passed deckid from the server.

        This function sends a get request to the server and retrieves the
        the deck with the passed id if the access right are sufficent.
        The passed deck will be converted to AnkipubSub objects
        for better handling during the creation of the cards.
        after the complete conversion a AnkipubSubDeck is returend.
        """
        # Kontrolliere ob zusätzliche Parameter übergeben wurden
        if kwargs:
            payload = kwargs.items()
        else:
            payload = {}

        self.login()  # Login

        # Führe get anfrage aus
        deckResponse = self.session.get(self.url+'/pull/deck/'+deckid,
                                        params=payload)

        # prüfe ob ne valid anfrage zurück kam
        if not deckResponse.status_code == requests.codes.ok:
            return None

        # Erzeuge aus der JSOn antwort ein Deck
        deck = AnkipubSubDeck.fromJsonObject(deckResponse.json())

        """Erzeuge aus den Karten in dieser Antwort AnkipupSub Objecte und\
         ersetze damit die Json Liste"""
        newNotes = []

        for note in deck.getNotes():
            newNotes.append(AnkipubSubNote(note))
        deck.update({'notes': newNotes})
        newModels = []
        for model in deck.get('models'):
            newModels.append(AnkipubSubModel(model))
        deck.update({'models': newModels})

        self.logout()
        return deck

    def login(self):
        """Send login credentials to the server and create seesion."""
        r = self.session.get(self.url+'/login',
                             auth=(self.username, self.password))

        if r.status_code == requests.codes.ok:
            return True
        else:
            print(r)
            raise Exception('401', 'Wrong Password or Username')

    def logout(self):
        """destroy the session on the server side."""
        self.session.get(self.url+'/logout')

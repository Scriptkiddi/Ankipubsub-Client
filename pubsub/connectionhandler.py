# !/usr/bin/python
#  -*- coding: utf-8 -*-
import requests
import json
from Deck import AnkipubSubDeck
from Note import AnkipubSubNote
from Model import AnkipubSubModel
from copy import deepcopy


class connectionHandler(object):

    def __init__(self, serverUrl, username, password):
        self.url = serverUrl
        self.password = password
        self.username = username
        self.session = requests.Session()
        # Session damit login Informationen mit gespeichert werden

    def push_deck(self, deck):
        deck = deepcopy(deck)
        self.login()  # Führe login durch

        notes = deck.get('notes')
        models = deck.get('models')
        """ Schreibe daten struktur um da die Karten eine eigene Klasse\
         sind die nur von UserDict geerbt hat"""
        for note in notes:
            notes[notes.index(note)] = note.data
        for model in models:
            models[models.index(model)] = model.data
        print(len(models))
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
        deckResponse = self.session.post(url,
                                         data=json.dumps(payload),
                                         headers=headers).json()

        deck = AnkipubSubDeck(deckResponse, deck.getLocalID())

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
        deck = AnkipubSubDeck(deckResponse.json())

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
        r = self.session.get(self.url+'/login',
                             auth=(self.username, self.password))

        if r.status_code == requests.codes.ok:
            return True
        else:
            print(r)
            raise Exception('401', 'Wrong Password or Username')

    def logout(self):
        self.session.get(self.url+'/logout')

#!/usr/bin/python
# -*- coding: utf-8 -*-
from UserDict import UserDict
from pubsub.util import (getRemoteDeckID,
                         getRemoteDeckLastChange,
                         getLocalDeckID,
                         convertToDatetime)
from aqt import mw
from Note import AnkipubSubNote
from Model import AnkipubSubModel
from anki.notes import Note
from anki.cards import Card
from copy import deepcopy
from datetime import datetime


class AnkipubSubDeck(UserDict):

    def __init__(self, notes, models, name, description,
                 lastChange, creationDate, remoteID=None, localDeckID=None):
        UserDict.__init__(self)
        self.setNotes(notes)
        self.setModels(models)
        self.setName(name)
        self.setDescription(description)
        self.setLastChange(lastChange)
        self.setRemoteID(remoteID)
        self.setLocalID(localDeckID)

    @classmethod
    def fromJsonObject(cls, deck):
        lastChange = convertToDatetime(str(deck.get('lastChange')))
        return cls(deck.get('notes'),
                   deck.get('models'),
                   deck.get('name'),
                   deck.get('description'),
                   lastChange,
                   deck.get('creationDate'),
                   deck.get('id'))
        #    self.update(deck)
        #    self.setLastChange(convertToDatetime(self.getLastChange()))

    @classmethod
    def fromLocalID(cls, localDeckID):
            col = mw.col
            """We create an ankiDeckManager because thats where\
             all the decks are stored"""
            ankiDeckManager = col.decks

            # After that we get the Deck we are intrested in
            ankiDeck = ankiDeckManager.get(localDeckID)

            # With this call we retrive all Card IDs
            ankiCardIDs = ankiDeckManager.cids(localDeckID)

            """with each id we create a anki Note object and\
             add it to a list for futher processing"""

            ankiNotes = []
            for cardID in ankiCardIDs:
                ankiNotes.append(Note(col, None, Card(col, cardID).nid))
            modelsDic = {}
            notes = []

            """for every note object we have we retrieve the model and create\
            a AnkiPubSubNote object we add the models to a dic so that we only\
            create models once and not for every note an extra model
            Model() 1 --> * Note()"""
            for note in ankiNotes:
                modelsDic.update({note.mid: note._model})
                notes.append(AnkipubSubNote(note, col))

            # For every Model in the dic we create a AnkipubSubModel
            models = []
            for modelID, model in modelsDic.items():

                """We deepcopy the model because otherwise with the next\
                commit we would change something in the users anki database"""
                model = deepcopy(model)

                """we move the anki assign id to localID because id is used\
                 by our server as a reference"""
                model.update({'localID': modelID})
                aModel = AnkipubSubModel(model)
                models.append(aModel)
            # Create a new Deck Object which we can push later to the server
            """
            we sort all the notes belonging to our deck after the mod value,
            the one with the biggest mod value is the one note last changed
            that change also represents the last change on our deck localy so
            we use this to generate a datetime stamp to compare to the last
            change on the server
            """
            ankiNotesByDate = sorted(ankiNotes, key=lambda note: note.mod)
            lastChange = datetime.fromtimestamp(ankiNotesByDate.pop().mod)
            creationDate = None
            remoteID = getRemoteDeckID(localDeckID)
            return cls(notes,
                       models,
                       ankiDeck.get('name'),
                       ankiDeck.get('desc'),
                       lastChange,
                       creationDate,
                       remoteID,
                       localDeckID)

            """# print(deck,localDeckID,notes,models,col)
            remoteDeckID = getRemoteDeckID(localDeckID)
            if remoteDeckID:
                self.update({'id': remoteDeckID})
            lastChange = getRemoteDeckLastChange(localDeckID)
            if lastChange:
                self.update({'lastChange': lastChange})

            self.update({'notes': notes})
            self.update({'models': models})"""

    def setRemoteID(self, deckID):
        self.update({'id': deckID})

    def getRemoteID(self):
        return self.get('id')

    def setLocalID(self, localDeckID):
        self.update({'localID': localDeckID})

    def getLocalID(self):
        return self.get('localID')

    def setName(self, name):
        self.update({'name': name})

    def getName(self):
        return self.get('name')

    def getNotes(self):
        return self.get('notes')

    def setNotes(self, notes):
        self.update({'notes': notes})

    def getModels(self):
        return self.get('models')

    def setModels(self, models):
        self.update({'models': models})

    def setDescription(self, description):
        self.update({'description': description})

    def setLastChange(self, lastChange):
        return self.update({'lastChange': lastChange})

    def getLastChange(self):
        return self.get('lastChange')

    def save(self, col, serverURL):
        col = mw.col
        models = self.get('models')
        notes = self.get('notes')
        localDeckID = col.decks.id(self.get('name'))
        col.decks.select(localDeckID)
        col.save()

        if self.get('id'):
            col.db.execute("INSERT OR REPLACE INTO DeckIDs\
             (RemoteID, LocalID, ServerURL) VALUES (?,?,?)", self.get('id'),
                           localDeckID, serverURL)
        for model in models:
            model.save(self.get('id'))
        for note in notes:
            note.save(self.get('id'))
        col.save()
        col.flush()

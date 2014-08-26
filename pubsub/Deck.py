#!/usr/bin/python
# -*- coding: utf-8 -*-
from UserDict import UserDict
from pubsub.util import getRemoteDeckID, getRemoteDeckLastChange, getLocalDeckID
from aqt import mw


class AnkipubSubDeck(UserDict):

    def __init__(self, deck, localDeckID=None, notes=None, models=None):
        UserDict.__init__(self)

        if deck:
            self.update(deck)
        else:
            # print(deck,localDeckID,notes,models,col)
            remoteDeckID = getRemoteDeckID(localDeckID)
            if remoteDeckID:
                self.update({'id': remoteDeckID})
            lastChange = getRemoteDeckLastChange(localDeckID)
            if lastChange:
                self.update({'lastChange': lastChange})

            self.update({'notes': notes})
            self.update({'models': models})
        if not localDeckID and self.get('id'):
            localDeckID = getLocalDeckID(self.get('id'))
        self.update({'localID': localDeckID})

    def setID(self, deckID):
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

#!/usr/bin/python
# -*- coding: utf-8 -*-
from UserDict import UserDict
from pubsub.util import getRemoteModelID, getLocalDeckID, getLocalModelID
from aqt import mw


class AnkipubSubModel(UserDict):
    def __init__(self, model):
        UserDict.__init__(self)
        self.update(model)
        self.update({'id': getRemoteModelID(self.get('localID'))})

    def setID(self, cardID):
        self.update({'id': cardID})

    def setLocalID(self, localCardID):
        self.update({'localID': localCardID})

    def getID(self):
        if self.get('id') is None:
            return False
        return self.get('id')

    def getLocalID(self):
        if self.get('localID') is None:
            return False
        return self.get('localID')

    def getCreationID(self):
        if self.get('creationCard') is None:
            return False
        return self.get('creationCard')

    def getOldCardID(self):
        if self.get('oldCard') is None:
            return False
        return self.get('oldCard')

    def getCreationDate(self):
        if self.get('creationDate') is None:
            return False
        return self.get('creationDate')

    def save(self, remoteDeckID):
        #How this works
        #check if exists
        #if so update
        #if not create new


        #Possiblitys for existing 
        #It exists on the server so create
        #It exists localy so update
        #if not self.get('localID'): #We dont have a localID for so it has to come from the server we create it

        #THIS IS FOR TESTING ONLY
        col = mw.col
        model = col.models.new(self.get('name'))
        for field in self.get('flds'):
            col.models.addField(model, field)
        model['req'] = self.get('req')
        model['tmpls'] = self.get('tmpls')
        model['latexPost'] = self.get('latexPost')
        model['usn'] = self.get('usn')
        model['sorft'] = self.get('sortf')
        model['css'] = self.get('css')
        model['type'] = self.get('type')
        model['tags'] = self.get('tags')
        model['latexPre'] = self.get('latexPre')
        model['did'] = getLocalDeckID(remoteDeckID)



        if not self.get('localID') and not getLocalModelID(self.get('creationModel')): #Wurde nicht gerade eben gepusht und ist nicht in der Lokalen Datenbank also neu
            col.models.add(model)
            col.save()
        elif self.get('localID')  and not getLocalModelID(self.get('creationModel')): #Hat ne lokale Id wurde also eben gepusht aber ist nicht in der Lokalen Datenbank also update
            model['id'] = self.get('localID')
            col.models.update(model)
        else:  # Hat nichts von allem also existiert schon also update
            model['id'] = getLocalModelID(self.get('creationModel'))
            col.models.update(model)
        mw.col.db.execute("INSERT OR REPLACE INTO ModelIDs (RemoteID, RemoteDeckID, LocalID) VALUES (?,?,?)", self.get('creationModel'), remoteDeckID, model['id'])

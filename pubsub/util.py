#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from aqt import mw


def getRemoteNoteID(localID):
    return mw.col.db.scalar("SELECT RemoteID FROM NoteIDs WHERE LocalID = ?",
                            localID)


def getLocalNoteID(remoteID):
    return mw.col.db.scalar("SELECT LocalID FROM NoteIDs WHERE RemoteID = ?",
                            remoteID)


def getRemoteModelID(localID):
    return mw.col.db.scalar("SELECT RemoteID FROM ModelIDs WHERE LocalID = ?",
                            localID)


def getLocalModelID(remoteID):
    return mw.col.db.scalar("SELECT LocalID FROM ModelIDs WHERE RemoteID = ?",
                            remoteID)


def getRemoteDeckID(localID):
    return mw.col.db.scalar("SELECT RemoteID FROM DeckIDs WHERE LocalID = ?",
                            localID)


def getLocalDeckID(remoteID):
    return mw.col.db.scalar("SELECT LocalID FROM DeckIDs WHERE RemoteID = ?",
                            remoteID)


def getRemoteDeckLastChange(localID):
    lastChange = mw.col.db.scalar("SELECT LastUpdate FROM DeckIDs\
    WHERE LocalID = ?",
                                  localID)
    if lastChange:
        return convertToDatetime(lastChange)
    return None


def convertToDatetime(string):
    try:
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")

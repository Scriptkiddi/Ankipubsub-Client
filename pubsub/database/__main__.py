#!/usr/bin/python
# -*- coding: utf-8 -*-
# import the main window object (mw) from ankiqt
from aqt import mw



def create_tables():
    """Create the Databases needed for the plugin."""
    print('we create the tables we need in your collection if they dont exist')
    mw.col.db.execute("CREATE TABLE IF NOT EXISTS Remote2LocalDeck(RemoteID INT PRIMARY KEY, LocalID INT)")
    mw.col.db.execute("CREATE TABLE IF NOT EXISTS RemoteDeck(ID INT PRIMARY KEY,\
RemoteID TEXT, ServerURL Text, read_password Text, writePassword Text, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")
   # mw.col.db.execute("CREATE TABLE IF NOT EXISTS NoteIDs(RemoteID INT PRIMARY KEY, RemoteDeckID INT, LocalID INT, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")
   # mw.col.db.execute("CREATE TABLE IF NOT EXISTS ModelIDs(RemoteID INT PRIMARY KEY, RemoteDeckID INT, LocalID INT, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")
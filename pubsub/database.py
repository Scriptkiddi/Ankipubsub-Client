#!/usr/bin/python
# -*- coding: utf-8 -*-
# import the main window object (mw) from ankiqt
from aqt import mw
from Deck import AnkipubSubDeck
from connectionhandler import connectionHandler


def createTables():
    """Create the Databases needed for the plugin."""
    print('we create the tables we need in your collection if they dont exist')
    mw.col.db.execute("CREATE TABLE IF NOT EXISTS DeckIDs(RemoteID INT PRIMARY KEY, LocalID INT, ServerURL TEXT, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")
    mw.col.db.execute("CREATE TABLE IF NOT EXISTS NoteIDs(RemoteID INT PRIMARY KEY, RemoteDeckID INT, LocalID INT, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")
    mw.col.db.execute("CREATE TABLE IF NOT EXISTS ModelIDs(RemoteID INT PRIMARY KEY, RemoteDeckID INT, LocalID INT, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")


def addRemoteDeck(remoteDeckID, serverURL, username, password):
    """Download a Remote Deck From the Server \
    and creates it in the local database."""
    createTables()
    # Create a Server handle to send the requests to
    server = connectionHandler(serverURL, username, password)
    print('Starting to add a Remote Deck with the id {0}'.format(remoteDeckID))
    # pull the remote Deck from the server with the passed rID

    remoteDeckPull = server.pull_deck(remoteDeckID)
    print(remoteDeckPull.getNotes())
    # Create the Deck
    remoteDeckPull.save(mw.col, serverURL)


def sync(localDeckID, serverURL, username, password, firsttime=True):
    """Syncronice a local deck with a remote deck."""
    col = mw.col
    col.flush()
    createTables()
    # Create a Server handle to send the requests to
    server = connectionHandler(serverURL, username, password)
    col = mw.col
    print("Starting sync")
    # Create a Deck object from the localDeckID
    localDeckToPush = AnkipubSubDeck.fromLocalID(localDeckID)
    # Check if we have a RemoteId for the deck
    # if not we assume the Deck doesnt exist on the server
    if not localDeckToPush.getRemoteID():

        print("The deck with the {0} did not have a RemoteId\
         so we push it to the server".format(localDeckID))
        # copy that stuff because server.push push does conversion magic
        remoteDeck = server.push_deck(localDeckToPush)

        """deepcopy that bitch because of conversion magic in serverupdate\
        UserDict-->Json and not back todo maybe do this in serverupdate not\
         sure but for now fuck it"""

        print('write new entry to DeckIDs RemoteId\
         = {0} localid = {1}'.format(remoteDeck.getRemoteID(), localDeckID))

        remoteDeck.save(mw.col, serverURL)
    else:  # deck exists
        print('The we are trying to sync\
        has following remote ID {0}'.format(localDeckToPush.getRemoteID()))
        """We pull the Deck from the Server to check if there\
         where any changes done"""
        remoteDeckPull = server.pull_deck(localDeckToPush.getRemoteID())
        """If the Date from the last Change on the Server is newer then the\
         Date we wrote in our Database local"""
        #
        print('Last Change on the Server\
         Deck {0}'.format(remoteDeckPull.getLastChange()))
        print('Last Change on the Local\
         Deck {0}'.format(localDeckToPush.getLastChange()))

        newNotes = False
        for note in localDeckToPush.getNotes():
            if not note.getRemoteID():
                newNotes = True

        if (remoteDeckPull.getLastChange() > localDeckToPush.getLastChange()) and firsttime:
            print('Deck on the Server is newer so we pull the deck')
            remoteDeckPull.save(col, serverURL)
            sync(localDeckID, serverURL, username, password, False)
            # We call sync again to push the local changes we made
        elif(newNotes):
            print('We have a newer deck so we push to the server')
            remoteDeckPush = server.push_deck(localDeckToPush)
            remoteDeckPush.save(col, serverURL)
        else:
            print('We have not added new Notes and the Server has no new notes for us so we dont do anything')


def download(localDeckID, serverURL, username, password):
    localDeckToPush = AnkipubSubDeck.fromLocalID(localDeckID)
    server = connectionHandler(serverURL, username, password)
    remoteDeckPull = server.pull_deck(localDeckToPush.getRemoteID())
    remoteDeckPull.save(mw.col, serverURL)


def upload(localDeckID, serverURL, username, password):
    localDeckToPush = AnkipubSubDeck.fromLocalID(localDeckID)
    server = connectionHandler(serverURL, username, password)
    remoteDeck = server.push_deck(localDeckToPush)
    remoteDeck.save()


def addUserToReadGroup(newUserName,
                       RemoteDeckID,
                       serverURL,
                       username,
                       password):
    server = connectionHandler(serverURL, username, password)
    server.addUserToReadGroup(newUserName, RemoteDeckID)


def addUserToWriteGroup(newUserName,
                        RemoteDeckID,
                        serverURL,
                        username,
                        password):
    server = connectionHandler(serverURL, username, password)
    server.addUserToWriteGroup(newUserName, RemoteDeckID)


def addUserToAdminGroup(newUserName,
                        RemoteDeckID,
                        serverURL,
                        username,
                        password):
    server = connectionHandler(serverURL, username, password)
    server.addUserToAdminGroup(newUserName, RemoteDeckID)


def getReadGroup(RemoteDeckID, serverURL, username, password):
    server = connectionHandler(serverURL, username, password)
    server.getReadGroup(RemoteDeckID)


def getAccessGroups(RemoteDeckID, serverURL, username, password):
    server = connectionHandler(serverURL, username, password)
    return server.getAccessGroups(RemoteDeckID)

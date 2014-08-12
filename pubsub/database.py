#!/usr/bin/python
# -*- coding: utf-8 -*-
# import the main window object (mw) from ankiqt
from aqt import mw

#from serverupdate import connectionHandler
from Deck import AnkipubSubDeck
from Note import AnkipubSubNote
from Model import AnkipubSubModel
from anki.decks import DeckManager
from anki.notes import Note
from anki.cards import Card
from connectionhandler import connectionHandler

from datetime import datetime
import locale

def createTables():
	"""Create the Databases needed for the plugin."""
	#Function to create Tabels if the plugin is run the first time
	print('we create the tables we need in your collection if they dont exist')
	mw.col.db.execute("CREATE TABLE IF NOT EXISTS DeckIDs(RemoteID INT PRIMARY KEY, LocalID INT, ServerURL TEXT, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")
	mw.col.db.execute("CREATE TABLE IF NOT EXISTS NoteIDs(RemoteID INT PRIMARY KEY, RemoteDeckID INT, LocalID INT, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")
	mw.col.db.execute("CREATE TABLE IF NOT EXISTS ModelIDs(RemoteID INT PRIMARY KEY, RemoteDeckID INT, LocalID INT, LastUpdate DATETIME DEFAULT CURRENT_TIMESTAMP)")

def deckToObject(deckID):
	"""Return a ÁnkiPubSubDeck with the given localID."""
	#We flush the collection so just in case something changed everything is in the database we work with
	col = mw.col
	col.flush()
	createTables()

	#If you read the functions above you will know we are not quite sure how anki exactly works
	#our test showed that this setup kind of works so we stick with it

	#We create an ankiDeckManager because thats where all the decks are stored
	ankiDeckManager = col.decks

	#After that we get the Deck we are intrested in
	ankiDeck = ankiDeckManager.get(deckID)

	#With this call we retrive all Card IDs
	ankiCardIDs = ankiDeckManager.cids(deckID)

	#with each id we create a anki Note object and add it to a list for futher processing

	ankiNotes = []
	for cardID in ankiCardIDs:
		ankiNotes.append(Note(col,None,Card(col,cardID).nid))


	modelsDic = {}
	notes = []

	#for every note object we have we retrieve the model and create a AnkiPubSubNote object
	# we add the models to a dic so that we only create models once and not for every note an extra model
	# Model() 1 --> * Note()
	for note in ankiNotes:
		modelsDic.update({note.mid : note._model})
		notes.append(AnkipubSubNote(note,col))

	#For every Model in the dic we create a AnkipubSubModel
	models = []
	for modelID, model in modelsDic.items():

		#We deepcopy the model because otherwise with the next commit we would change something in the users anki database
		model = deepcopy(model)

		#we move the anki assign id to localID because id is used by our server as a reference
		model.update({'localID':modelID})
		aModel = AnkipubSubModel(model)
		models.append(aModel)
	#Create a new Deck Object which we can push later to the server
	deckObject = AnkipubSubDeck(None,deckID,notes,models)

	deckObject.setName(ankiDeck.get('name'))
	deckObject.setDescription(ankiDeck.get('desc'))

	return deckObject

def addRemoteDeck(remoteDeckID,serverURL,username,password):
	"""Download a Remote Deck From the Server and creates it in the local database."""
	createTables()
	#Create a Server handle to send the requests to
	server = connectionHandler(serverURL,username,password)
	print('Starting to add a Remote Deck with the id {0}'.format(remoteDeckID))
	#pull the remote Deck from the server with the passed rID

	remoteDeckPull = server.pull_deck(remoteDeckID)
	#Create the Deck
	remoteDeckPull.save(mw.col,serverURL)

def sync(localDeckID, serverURL, username, password, firsttime=True):
	"""Syncronice a local deck with a remote deck."""
	#Create a Server handle to send the requests to
	server = connectionHandler(serverURL,username,password)
	col = mw.col
	print("Starting sync")
	#Create a Deck object from the localDeckID
	localDeckToPush = deckToObject(localDeckID)
	#Check if we have a RemoteId for the deck
	#if not we assume the Deck doesnt exist on the server
	if not localDeckToPush.getRemoteID():

		print("The deck with the {0} did not have a RemoteId so we push it to the server".format(localDeckID))
		#copy that stuff because server.push push does conversion magic
		
		remoteDeck = server.push_deck(localDeckToPush)

		#deepcopy that bitch because of conversion magic in serverupdate UserDict-->Json and not back
		#todo maybe do this in serverupdate not sure but for now fuck it

		print('write new entry to DeckIDs RemoteId = {0} localid = {1}'.format(remoteDeck.getRemoteID(), localDeckID))

		remoteDeck.save(mw.col,serverURL)
	else: #deck exists
		print('The we are trying to sync has following remote ID {0}'.format(localDeckToPush.getRemoteID()))
		#We pull the Deck from the Server to check if there where any changes done
		remoteDeckPull = server.pull_deck(localDeckToPush.getRemoteID())
		#If the Date from the last Change on the Server is newer then the Date we wrote in our Database local
		#
		print('Last Change on the Server Deck {0}'.format(remoteDeckPull.getLastChange()))
		print('Last Change on the Local Deck {0}'.format(localDeckToPush.getLastChange()))

		lastChange = remoteDeckPull.getLastChange()[:-4] #-4 to get rid of the gtm at the end of the string

		#OK from here on its fucking dirty watch where you step your mileage may vary
		#oldLocal = locale.getlocale(locale.LC_TIME);
		#locale.setlocale(locale.LC_TIME, (None,None))
		#lastChange = datetime.strptime(lastChange, "%Y-%m-%d %H:%M:%S.%f")
		#remoteDeckPull.setLastChange(lastChange)
		#For all those who have not wanderd the path of date convertion enligthment here is why we do this
		#Anki sets the lokals when you select your language and python is retarded and think oh hey lets
		#make our timestamps fit to that local so if you are german strftime('%a') returns Di(Dienstag) instead of Tue(Tuesday)
		#to make sure we are on the same date as my server is we drop every local settings for the date conversion
		#and then reapply them

		#locale.setlocale(locale.LC_TIME, oldLocal)
		#ITS DIRTY ITS NOT BEUTIFUL BUT IT WORKS

		if (remoteDeckPull.getLastChange() > localDeckToPush.getLastChange()) and firsttime:
			print('Deck on the Server is newer so we pull the deck')
			remoteDeckPull.save(col, serverURL)
			sync(localDeckID, serverURL, username, password, False)
			#We call sync again to push the local changes we made
		else:
			print('We have a newer deck so we push to the server')
			remoteDeckPush = server.push_deck(localDeckToPush)
			remoteDeckPush.save(col, serverURL)

from anki.hooks import wrap
from aqt.preferences import Preferences
from aqt.deckbrowser import DeckBrowser
from aqt.utils import askUserDialog, openLink, showInfo, getOnlyText
from aqt.qt import *
from aqt import mw
import aqt
from permissions import Ui_Dialog
from aqt.qt import debug
from database import sync, addRemoteDeck
from pubsub import util


def setupAnkiPubSub(self):
    """Add options to the preferences menu."""
    global ankipubsubenable
    global ankipubsubName
    global ankipubsubPassword

    container = self.form.tab_2.layout().children()[0].children()[0]
    groupBox = QGroupBox("enable")
    layout = QVBoxLayout()

    ankipubsubenable = QCheckBox("AnkiPubSub", self)
    ankipubsubenable.setChecked(mw.col.conf.get('pubSubEnabled', False))

    ankipubsubNameLabel = QLabel("Username:")
    ankipubsubName = QLineEdit()
    ankipubsubName.setText(mw.col.conf.get('pubSubName', ""))

    ankipubsubPasswordLabel = QLabel("Password:")
    ankipubsubPassword = QLineEdit()
    ankipubsubPassword.setText(mw.col.conf.get('pubSubPassword',""))
    ankipubsubPassword.setEchoMode(QLineEdit.Password)

    layout.insertWidget(1, ankipubsubenable)
    layout.insertWidget(2, ankipubsubNameLabel)
    layout.insertWidget(3, ankipubsubName)
    layout.insertWidget(4, ankipubsubPasswordLabel)
    layout.insertWidget(5, ankipubsubPassword)

    ankipubsubenable.stateChanged.connect(pubSubEnable)
    ankipubsubName.connect(ankipubsubName, SIGNAL("editingFinished()"), updateName)
    ankipubsubPassword.connect(ankipubsubPassword, SIGNAL("editingFinished()"), updatePassword)

    groupBox.setLayout(layout)
    container.insertWidget(int(layout.count())+1, groupBox)


def pubSubEnable():
    """Update the config with values from the preferences menu."""
    mw.col.conf['pubSubEnabled'] = ankipubsubenable.isChecked()


def updateName():
    """Update config with values from the menu."""
    mw.col.conf['pubSubName'] = ankipubsubName.text()


def updatePassword():
    """Update pubSubPassword with value from menu."""
    mw.col.conf['pubSubPassword'] = ankipubsubPassword.text()


def myShowOptions(self, did):
    """Overwrite the standard options."""
    #standard options:
    m = QMenu(self.mw)
    a = m.addAction(_("Rename"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._reankipubsubName(did))
    a = m.addAction(_("Options"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._options(did))
    a = m.addAction(_("Delete"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._delete(did))
    #share with pubsub
    a = m.addAction(_("Share with PubSub"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: share(did))
    m.exec_(QCursor.pos())


def myOnShared(self):
    """Add a button to the shared menu."""
    choice = askUserDialog("Choose source", [QPushButton("AnkiWeb"), QPushButton("PubSub")]).run()
    if choice == "AnkiWeb":
            openLink(aqt.appShared+"decks/")
    elif choice == "PubSub":
            remoteDid = getOnlyText("Provide a remote deck-ID")
            print("remoteDid = " + remoteDid)
            #TODO: call with proper arguments
            addRemoteDeck(remoteDid,"http://144.76.172.187:5000/v0",mw.col.conf.get('pubSubName', ""),mw.col.conf.get('pubSubPassword',""))

def share(did):
    """Share a deck with the server."""
    try:
        sync(did,"http://144.76.172.187:5000/v0",mw.col.conf.get('pubSubName', ""),mw.col.conf.get('pubSubPassword',""))
    except Exception as e:
        showInfo("There was a problem sharing your deck. \n"+str(e))

    d = QDialog()
    d.ui = Ui_Dialog()
    d.ui.setupUi(d)
    d.ui.remoteDeckID.setText(str(util.getRemoteDeckID(did)))
    d.exec_()

Preferences.setupNetwork = wrap(Preferences.setupNetwork, setupAnkiPubSub)

DeckBrowser._showOptions = myShowOptions
DeckBrowser._onShared = myOnShared

from anki.hooks import wrap
from aqt.preferences import Preferences
from aqt.deckbrowser import DeckBrowser
from aqt.utils import askUserDialog, openLink, showInfo, getOnlyText, shortcut
from aqt.qt import *
from aqt import mw
import aqt
from permissions import Ui_Dialog
from database import sync, addRemoteDeck, download
from pubsub import util
from deckmanagerUI import Ui_Form
from PyQt4 import QtCore, QtGui
from Deck import AnkipubSubDeck

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
    ankipubsubPassword.setText(mw.col.conf.get('pubSubPassword', ""))
    ankipubsubPassword.setEchoMode(QLineEdit.Password)

    layout.insertWidget(1, ankipubsubenable)
    layout.insertWidget(2, ankipubsubNameLabel)
    layout.insertWidget(3, ankipubsubName)
    layout.insertWidget(4, ankipubsubPasswordLabel)
    layout.insertWidget(5, ankipubsubPassword)

    ankipubsubenable.stateChanged.connect(pubSubEnable)
    ankipubsubName.connect(ankipubsubName,
                           SIGNAL("editingFinished()"),
                           updateName)
    ankipubsubPassword.connect(ankipubsubPassword,
                               SIGNAL("editingFinished()"),
                               updatePassword)

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
            if remoteDid:
                print("remoteDid = " + remoteDid)
                try:
                    addRemoteDeck(remoteDid, "http://144.76.172.187:5000/v0",
                                  mw.col.conf.get('pubSubName', ""),
                                  mw.col.conf.get('pubSubPassword', ""))
                except Exception:
                    showInfo("You entered a wrong user name or password please try again.")


def share(did):
    """Share a deck with the server."""
    try:
        sync(did,
             "http://144.76.172.187:5000/v0",
             mw.col.conf.get('pubSubName', ""),
             mw.col.conf.get('pubSubPassword', "")
             )
    except Exception as e:
        showInfo("There was a problem sharing your deck. \n"+str(e))

    d = QDialog()
    d.ui = Ui_Dialog()
    d.ui.setupUi(d)
    d.ui.remoteDeckID.setText(str(util.getRemoteDeckID(did)))
    d.exec_()


class AnkiPubSubDeckManagerTableViewModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.arraydata[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        return None

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))


def ankiDeckManagerSetup():
    """
    Configure the Ui_Dialog.

    This function starts with collecting the data
    needed to fill the table in the ui, then
    straps it all together and exec it to present
    it to the user.
    """
    # create an cell widget

    header = ['Deck', 'Deck Remote ID', '']

    f = QDialog()
    f.ui = Ui_Form()
    f.ui.setupUi(f)
    table = f.ui.tableWidget
    decks = util.getAllAnkiPubSubDecks()
    table.setRowCount(len(decks))
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(header)
    for (i, deck) in enumerate(decks):
        did = deck[1]

        deck = AnkipubSubDeck.fromLocalID(did)
        widget = QWidget(table)
        btnDelete = QPushButton(widget)
        btnDelete.setGeometry(0, 0, 20, 20)
        btnDownload = QPushButton(widget)
        btnDownload.setGeometry(20, 0, 20, 20)
        btnDownload.clicked.connect(
            lambda: download(did,
                             mw.col.conf.get('ankipubsubServer',
                                             "http://144.76.172.187:5000/v0"),
                             mw.col.conf.get('pubSubName', ""),
                             mw.col.conf.get('pubSubPassword', "")))
        btnUpload = QPushButton(widget)
        btnUpload.setText('Upload')
        btnUpload.setGeometry(40, 0, 20, 20)
        btnSettings = QPushButton(widget)
        btnSettings.setText('Settings')
        btnSettings.setGeometry(60, 0, 20, 20)
        btnSettings.clicked.connect(lambda: showInfo())
        table.setCellWidget(i, 2, widget)
        table.setItem(i, 0, QTableWidgetItem(str(deck.getName())))
        table.setItem(i, 1, QTableWidgetItem(str(deck.getRemoteID())))

    f.exec_()


def ankiDeckSettings(did):



def test(self):
    links = [
        ["", "ankipubsubDeckManager", _("AnkiPubSub")],
        ["", "shared", _("Get Shared")],
        ["", "create", _("Create Deck")],
        ["Ctrl+I", "import", _("Import File")],
    ]
    buf = ""
    for b in links:
        if b[0]:
            b[0] = _("Shortcut key: %s") % shortcut(b[0])
        buf += """
<button title='%s' onclick='py.link(\"%s\");'>%s</button>""" % tuple(b)
    self.bottom.draw(buf)
    if isMac:
        size = 28
    else:
        size = 36 + self.mw.fontHeightDelta*3
    self.bottom.web.setFixedHeight(size)
    self.bottom.web.setLinkHandler(self._linkHandler)


def ankiPubSubLinkHandler(self, url, **kwargs):
    """
    wrap around the normal Link Handler.

    It checks for the signals we expect for the buttons we placed in the gui
    if it cant find a single that it needs to trigger on it passes
    it to the normal _linkHandler function.
    """
    if ":" in url:
        (cmd, arg) = url.split(":")
    else:
        cmd = url

    if cmd == "ankipubsubDeckManager":
        ankiDeckManagerSetup()
    else:
        kwargs.get('_old')(self, url)


DeckBrowser._drawButtons = wrap(DeckBrowser._drawButtons, test)

DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler,
                                ankiPubSubLinkHandler,
                                pos='around')
Preferences.setupNetwork = wrap(Preferences.setupNetwork, setupAnkiPubSub)

DeckBrowser._showOptions = myShowOptions
DeckBrowser._onShared = myOnShared

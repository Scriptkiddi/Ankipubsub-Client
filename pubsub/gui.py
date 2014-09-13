from anki.hooks import wrap
from aqt.preferences import Preferences
from aqt.deckbrowser import DeckBrowser
from aqt.utils import askUserDialog, openLink, showInfo, getOnlyText, shortcut
from aqt.qt import *
from aqt import mw
import aqt
from permissions import Ui_Dialog
from database import sync, addRemoteDeck, download, getAccessGroups, addUserToReadGroup, addUserToWriteGroup, addUserToAdminGroup
from pubsub import util
from deckmanagerUI import AnkiPubSubDeckManagerUI
from deck_settings import Ui_Form
from PyQt4 import QtGui
from Deck import AnkipubSubDeck
from ankipubsub_settings import AnkiPubSubSettingsUI
from functools import partial


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
    # standard options:
    m = QMenu(self.mw)
    a = m.addAction(_("Rename"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._reankipubsubName(did))
    a = m.addAction(_("Options"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._options(did))
    a = m.addAction(_("Delete"))
    a.connect(a, SIGNAL("triggered()"), lambda did=did: self._delete(did))
    # share with pubsub
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


def ankiDeckManagerSetup():
    """
    Configure the Ui_Dialog.

    This function starts with collecting the data
    needed to fill the table in the ui, then
    straps it all together and exec it to present
    it to the user.
    """
    # create an cell widget

    f = QDialog()
    f.ui = AnkiPubSubDeckManagerUI()
    f.ui.setupUi(f)

    f.ui.ankiPubSubSettings.clicked.connect(lambda: ankiPubSubSettings())
    table = f.ui.tableWidget
    decks = util.getAllAnkiPubSubDecks()
    table.setRowCount(len(decks))
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Deck', 'Deck Remote ID', ''])
    table.setColumnWidth(0, 160)
    table.setColumnWidth(1, 200)
    table.setColumnWidth(2, 120)

    for (i, deck) in enumerate(decks):
        did = deck[1]

        deck = AnkipubSubDeck.fromLocalID(did)
        deckRemoteID = deck.getRemoteID()
        widget = QWidget(table)
        btnDelete = QPushButton(widget)
        btnDelete.setGeometry(0, 0, 30, 30)
        btnDelete.setIcon(QIcon('/home/fritz/code/radical-dreamers/Ankipubsub-Client/pubsub/images/Delete-Resized.jpg'))
        btnDelete.setIconSize(QSize(25, 25))

        btnDownload = QPushButton(widget)
        btnDownload.setGeometry(30, 0, 30, 30)
        # TODO FIX TO PARTIAL
        btnDownload.clicked.connect(
            lambda: download(did,
                             mw.col.conf.get('ankipubsubServer',
                                             "http://144.76.172.187:5000/v0"),
                             mw.col.conf.get('pubSubName', ""),
                             mw.col.conf.get('pubSubPassword', "")))
        btnDownload.setIcon(QIcon('/home/fritz/code/radical-dreamers/Ankipubsub-Client/pubsub/images/Download-Resized.jpg'))
        btnDownload.setIconSize(QSize(25, 25))

        btnUpload = QPushButton(widget)
        btnUpload.setGeometry(60, 0, 30, 30)
        btnUpload.setIcon(QIcon('/home/fritz/code/radical-dreamers/Ankipubsub-Client/pubsub/images/Upload-Resized.jpg'))
        btnUpload.setIconSize(QSize(25, 25))

        btnSettings = QPushButton(widget)
        btnSettings.setGeometry(90, 0, 30, 30)
        btnSettings.setIcon(QIcon('/home/fritz/code/radical-dreamers/Ankipubsub-Client/pubsub/images/Settings-Resized.jpg'))
        btnSettings.setIconSize(QSize(25, 25))
        btnSettings.clicked.connect(partial(ankiDeckSettings, did=deckRemoteID))
        table.setCellWidget(i, 2, widget)
        table.setItem(i, 0, QTableWidgetItem(str(deck.getName())))
        table.setItem(i, 1, QTableWidgetItem(str(deck.getRemoteID())))
    f.exec_()

def ankiPubSubSettingsSave(form):
    # f.ui.username
    mw.col.conf['pubSubPassword'] = form.ui.username.text()
    mw.col.conf['pubSubName'] = form.ui.password.text()

def ankiPubSubSettings():
    f = QDialog()
    f.ui = AnkiPubSubSettingsUI()
    f.ui.setupUi(f)
    f.ui.username.setText(mw.col.conf.get('pubSubName', ""))
    f.ui.password.setText(mw.col.conf.get('pubSubPassword', ""))
    f.ui.Login.clicked.connect(partial(ankiPubSubSettingsSave, form=f))
    f.exec_()


def addUser(table):
    i = table.rowCount()
    table.insertRow(i)
    isAdmin = QtGui.QCheckBox(table)
    canWrite = QtGui.QCheckBox(table)
    canRead = QtGui.QCheckBox(table)
    table.setCellWidget(i, 1, canRead)
    table.setCellWidget(i, 2, canWrite)
    table.setCellWidget(i, 3, isAdmin)


def deckSettingsSave(table, users, did):
    # If we have more rows then users we added a User to the Deck
    if table.rowCount() > len(users):
        for i in range(0, table.rowCount()):
            if table.item(i, 0) is not None and table.item(i, 0).text() not in users:
                if table.cellWidget(i, 1).isChecked():
                    addUserToReadGroup(table.item(i, 0).text(), did,
                                       mw.col.conf.get('ankipubsubServer',
                                                       "http://144.76.172.187:5000/v0"),
                                       mw.col.conf.get('pubSubName', ""),
                                       mw.col.conf.get('pubSubPassword', ""))
                if table.cellWidget(i, 2).isChecked():
                    addUserToWriteGroup(table.item(i, 0).text(), did,
                                        mw.col.conf.get('ankipubsubServer',
                                                       "http://144.76.172.187:5000/v0"),
                                        mw.col.conf.get('pubSubName', ""),
                                        mw.col.conf.get('pubSubPassword', ""))
                if table.cellWidget(i, 3).isChecked():
                    addUserToAdminGroup(table.item(i, 0).text(), did,
                                        mw.col.conf.get('ankipubsubServer',
                                                       "http://144.76.172.187:5000/v0"),
                                        mw.col.conf.get('pubSubName', ""),
                                        mw.col.conf.get('pubSubPassword', ""))
    else:
        pass


def ankiDeckSettings(did):
    f = QDialog()
    f.ui = Ui_Form()
    f.ui.setupUi(f)
    table = f.ui.tableWidget
    groups = getAccessGroups(did,
                             mw.col.conf.get('ankipubsubServer',
                                             "http://144.76.172.187:5000/v0"),
                             mw.col.conf.get('pubSubName', ""),
                             mw.col.conf.get('pubSubPassword', ""))
    users = {}
    for user in groups.get('readGroup'):
        if user not in users:
            users[user] = 1
        else:
            users[user] += 1

    for user in groups.get('writeGroup'):
        if user not in users:
            users[user] = 1
        else:
            users[user] += 1

    for user in groups.get('adminGroup'):
        if user not in users:
            users[user] = 1
        else:
            users[user] += 1
    table.setColumnCount(4)
    table.setRowCount(len(users))
    for (i, user) in enumerate(users):
        isAdmin = QtGui.QCheckBox(table)
        canWrite = QtGui.QCheckBox(table)
        canRead = QtGui.QCheckBox(table)
        if users[user] >= 1:
            canRead.setChecked(True)
        if users[user] >= 2:
            canWrite.setChecked(True)
        if users[user] >= 3:
            isAdmin.setChecked(True)
        table.setItem(i, 0, QTableWidgetItem(str(user)))
        table.setCellWidget(i, 1, canRead)
        table.setCellWidget(i, 2, canWrite)
        table.setCellWidget(i, 3, isAdmin)

    table.setHorizontalHeaderLabels(['Name', 'Read', 'Write', 'Admin'])
    table.resizeColumnsToContents()

    f.ui.AddUser.clicked.connect(lambda: addUser(table))
    f.ui.Abort.clicked.connect(lambda: f.done(0))
    f.ui.Save.clicked.connect(lambda: deckSettingsSave(table, users, did))
    f.exec_()


def ankiPubSubOptionsButton(self):
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


DeckBrowser._drawButtons = wrap(DeckBrowser._drawButtons,
                                ankiPubSubOptionsButton)

DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler,
                                ankiPubSubLinkHandler,
                                pos='around')

from anki.hooks import wrap
from aqt.deckbrowser import DeckBrowser
from aqt.utils import askUserDialog, openLink, showInfo, getOnlyText, shortcut
from aqt.qt import *
from aqt import mw
import aqt
from permissions import Ui_Dialog
from database import (sync,
                      addRemoteDeck,
                      download,
                      upload,
                      getAccessGroups,
                      addUserToReadGroup,
                      removeUserFromReadGroup,
                      addUserToWriteGroup,
                      removeUserFromWriteGroup,
                      addUserToAdminGroup,
                      removeUserFromAdminGroup,
                      createTables
                      )
from pubsub import util
from deckmanagerUI import Ui_AnkiPubSubDeckManager
from deck_settings import Ui_Form
from PyQt4 import QtGui
from Deck import AnkipubSubDeck
from ankipubsub_settings import AnkiPubSubSettingsUI
from functools import partial
from Queue import Queue




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


def addRemoteDeckButton(form):
    remoteID = form.ui.remoteDeckId.text()
    if not len(remoteID) == 24:
        showInfo('This seems is not a valid Remote Deck ID please try again')
        return
    addRemoteDeck(remoteID, "http://144.76.172.187:5000/v0",
                  mw.col.conf.get('pubSubName', ""),
                  mw.col.conf.get('pubSubPassword', ""))
    drawTable(form)


def deleteAnkiPubSubDeck(form, remoteID):
    util.deleteAnkiPubSubDeck(remoteID)
    drawTable(form)


def drawTable(f):
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

        btnDelete.setIcon(QIcon('../../addons/pubsub/images/Delete-Resized.jpg'))
        btnDelete.setIconSize(QSize(25, 25))
        btnDelete.clicked.connect(partial(deleteAnkiPubSubDeck,form=f, remoteID=deckRemoteID))
        btnDownload = QPushButton(widget)
        btnDownload.setGeometry(30, 0, 30, 30)
        # TODO FIX TO PARTIAL
        btnDownload.clicked.connect(
            partial(download, did,
                    mw.col.conf.get('ankipubsubServer',
                                    "http://144.76.172.187:5000/v0"),
                    mw.col.conf.get('pubSubName', ""),
                    mw.col.conf.get('pubSubPassword', "")))
        btnDownload.setIcon(QIcon('../../addons/pubsub/images/Download-Resized.jpg'))
        btnDownload.setIconSize(QSize(25, 25))

        btnUpload = QPushButton(widget)
        btnUpload.setGeometry(60, 0, 30, 30)
        btnUpload.setIcon(QIcon('../../addons/pubsub/images/Upload-Resized.jpg'))
        btnUpload.setIconSize(QSize(25, 25))
        btnUpload.clicked.connect(
            partial(upload, did,
                    mw.col.conf.get('ankipubsubServer',
                                    "http://144.76.172.187:5000/v0"),
                    mw.col.conf.get('pubSubName', ""),
                    mw.col.conf.get('pubSubPassword', "")))

        btnSettings = QPushButton(widget)
        btnSettings.setGeometry(90, 0, 30, 30)
        btnSettings.setIcon(QIcon('../../addons/pubsub/images/Settings-Resized.jpg'))
        btnSettings.setIconSize(QSize(25, 25))
        btnSettings.clicked.connect(partial(ankiDeckSettings, did=deckRemoteID))
        table.setCellWidget(i, 2, widget)
        table.setItem(i, 0, QTableWidgetItem(str(deck.getName())))
        table.setItem(i, 1, QTableWidgetItem(str(deck.getRemoteID())))


def ankiDeckManagerSetup():
    """
    Configure the Ui_Dialog.

    This function starts with collecting the data
    needed to fill the table in the ui, then
    straps it all together and exec it to present
    it to the user.
    """
    # create an cell widget
    createTables()
    f = QDialog()
    f.ui = Ui_AnkiPubSubDeckManager()
    f.ui.setupUi(f)

    f.ui.ankiPubSubSettings.clicked.connect(lambda: ankiPubSubSettings())
    drawTable(f)

    f.ui.ankiPubSubAddDeck.clicked.connect(partial(addRemoteDeckButton, form=f))
    f.exec_()


def ankiPubSubSettingsSave(form):
    # f.ui.username
    mw.col.conf['pubSubName'] = form.ui.username.text()
    mw.col.conf['pubSubPassword'] = form.ui.password.text()
    form.done(0)


def ankiPubSubSettings():
    f = QDialog()
    f.ui = AnkiPubSubSettingsUI()
    f.ui.setupUi(f)
    f.ui.username.setText(mw.col.conf.get('pubSubName', ""))
    f.ui.password.setEchoMode(QLineEdit.Password)
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


def deckSettingsSave(table, users, did, changes, form):
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
    while not changes.empty():
        checkbox = changes.get()
        username = table.item(checkbox[0], 0).text()
        if checkbox[1] == 3:
            if checkbox[2].isChecked():
                addUserToAdminGroup(username, did,
                                    mw.col.conf.get('ankipubsubServer',
                                                    "http://144.76.172.187:5000/v0"),
                                    mw.col.conf.get('pubSubName', ""),
                                    mw.col.conf.get('pubSubPassword', ""))
            else:
                removeUserFromAdminGroup(username, did,
                                         mw.col.conf.get('ankipubsubServer',
                                                         "http://144.76.172.187:5000/v0"),
                                         mw.col.conf.get('pubSubName', ""),
                                         mw.col.conf.get('pubSubPassword', ""))
        elif checkbox[1] == 2:
            if checkbox[2].isChecked():
                addUserToWriteGroup(username, did,
                                    mw.col.conf.get('ankipubsubServer',
                                                    "http://144.76.172.187:5000/v0"),
                                    mw.col.conf.get('pubSubName', ""),
                                    mw.col.conf.get('pubSubPassword', ""))
            else:
                removeUserFromWriteGroup(username, did,
                                         mw.col.conf.get('ankipubsubServer',
                                                         "http://144.76.172.187:5000/v0"),
                                         mw.col.conf.get('pubSubName', ""),
                                         mw.col.conf.get('pubSubPassword', ""))
        else:
            if checkbox[2].isChecked():
                addUserToReadGroup(username, did,
                                   mw.col.conf.get('ankipubsubServer',
                                                   "http://144.76.172.187:5000/v0"),
                                   mw.col.conf.get('pubSubName', ""),
                                   mw.col.conf.get('pubSubPassword', ""))
            else:
                removeUserFromReadGroup(username, did,
                                        mw.col.conf.get('ankipubsubServer',
                                                         "http://144.76.172.187:5000/v0"),
                                        mw.col.conf.get('pubSubName', ""),
                                        mw.col.conf.get('pubSubPassword', ""))
    form.done(0)


def uniqueList(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def ankiDeckSettings(did):
    f = QDialog()
    f.ui = Ui_Form()
    f.ui.setupUi(f)
    table = f.ui.tableWidget
    changes = Queue()
    groups = getAccessGroups(did,
                             mw.col.conf.get('ankipubsubServer',
                                             "http://144.76.172.187:5000/v0"),
                             mw.col.conf.get('pubSubName', ""),
                             mw.col.conf.get('pubSubPassword', ""))
    #users = uniqueList(groups.get('readGroup').append(groups.get('writeGroup').append(groups.get('adminGroup'))))
    readGroup = groups.get('readGroup') if groups.get('readGroup') else []
    writeGroup = groups.get('writeGroup') if groups.get('writeGroup') else []
    adminGroup = groups.get('adminGroup') if groups.get('adminGroup') else []
    users = uniqueList(readGroup + writeGroup + adminGroup)

    table.setColumnCount(4)
    table.setRowCount(len(users))
    for (i, user) in enumerate(users):
        isAdmin = QtGui.QCheckBox(table)
        canWrite = QtGui.QCheckBox(table)
        canRead = QtGui.QCheckBox(table)
        if user in readGroup:
            canRead.setChecked(True)
        if user in writeGroup:
            canWrite.setChecked(True)
        if user in adminGroup:
            isAdmin.setChecked(True)

        table.setItem(i, 0, QTableWidgetItem(str(user)))
        isAdmin.connect(isAdmin, SIGNAL("stateChanged(int)"), partial(changes.put, (i, 3, isAdmin)))
        canWrite.connect(canWrite, SIGNAL("stateChanged(int)"), partial(changes.put, (i, 2, canWrite)))
        canRead.connect(canRead, SIGNAL("stateChanged(int)"), partial(changes.put, (i, 1, canRead)))
        table.setCellWidget(i, 1, canRead)
        table.setCellWidget(i, 2, canWrite)
        table.setCellWidget(i, 3, isAdmin)

        """btnDelete = QPushButton(table)
        btnDelete.setGeometry(0, 0, 30, 30)

        btnDelete.setIcon(QIcon('../../addons/pubsub/images/Delete-Resized.jpg'))
        btnDelete.setIconSize(QSize(25, 25))
        btnDelete.clicked.connect(partial(table.removeRow, i))
        table.setCellWidget(i, 4, btnDelete)"""

    table.setHorizontalHeaderLabels(['Name', 'Read', 'Write', 'Admin', 'Delete'])
    table.resizeColumnsToContents()

    f.ui.AddUser.clicked.connect(lambda: addUser(table))
    f.ui.Abort.clicked.connect(lambda: f.done(0))
    f.ui.Save.clicked.connect(lambda: deckSettingsSave(table, users, did, changes, f))
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
DeckBrowser._showOptions = myShowOptions

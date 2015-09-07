__author__ = 'fritz'
from functools import partial
from Queue import Queue
from aqt import mw

#from permissions import Ui_Dialog
from pubsub.database.__main__ import create_tables
from aqt.utils import askUserDialog, openLink, showInfo, getOnlyText, shortcut
from .draw import drawTable
from .auto_gen.ankipubsub_settings import Ui_Form as Ui_ankipubsub_settings
from .auto_gen.deck_settings import Ui_Form as Ui_deck_settings
from .auto_gen.deckmanager import Ui_AnkiPubSubDeckManager
from .auto_gen.publish_deck import Ui_publishDeckForm
from .buttons import addRemoteDeckButton
from PyQt4.QtGui import QDialog




def deleteAnkiPubSubDeck(form, remoteID):
    util.deleteAnkiPubSubDeck(remoteID)
    drawTable(form)





def publishDeckGui(ankiDeckForm):
    f = QDialog()
    f.ui = Ui_publishDeckForm()
    f.ui.setupUi(f)
    f.ui.pushButtonPublishDeck.clicked.connect(partial(publishDeckGuiOk, f, ankiDeckForm))
    f.ui.comboBox.addItems(mw.col.decks.allNames())
    f.ui.pushButtonCancel.clicked.connect(lambda: f.done(0))
    f.exec_()


def publishDeckGuiOk(form, ankiDeckForm):
    selectedDeck = str(form.ui.comboBox.currentText())
    localDeckID = mw.col.decks.id(selectedDeck, False)
    readPassword = form.ui.readPassword.text()
    writePassword = form.ui.writePassword.text()
    showInfo(readPassword)
    publish(localDeckID,
           mw.col.conf.get('ankipubsubServer',
                           "http://144.76.172.187:5000/v0"),
           mw.col.conf.get('pubSubName', ""),
           mw.col.conf.get('pubSubPassword', ""), readPassword, writePassword)
    drawTable(ankiDeckForm)
    form.done(0)


def anki_deck_manager_setup():
    """
    Configure the Ui_Dialog.

    This function starts with collecting the data
    needed to fill the table in the ui, then
    straps it all together and exec it to present
    it to the user.
    """
    if not mw.col.conf.get('pubSupFirstRun', ""):

        create_tables()
        ankiPubSubSettings()  # Open username and passwor dialog
        mw.col.conf['pubSupFirstRun'] = "True"
        mw.col.save()
        mw.col.db.commit()
    # create an cell widget

    f = QDialog()
    f.ui = Ui_AnkiPubSubDeckManager()
    f.ui.setupUi(f)

    f.ui.ankiPubSubSettings.clicked.connect(lambda: ankiPubSubSettings())  # Wireup username and passwor dialog
    f.ui.publishDeck.clicked.connect(partial(publishDeckGui, f))
    drawTable(f)  # draws the table for the decks
    f.ui.ankiPubSubAddDeck.clicked.connect(partial(addRemoteDeckButton, f))  # subscribe to remote deck button
    f.exec_()


def ankiPubSubSettingsSave(form):
    # f.ui.username
    mw.col.conf['pubSubName'] = form.ui.username.text()
    mw.col.conf['pubSubPassword'] = form.ui.password.text()
    mw.col.flush()
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
    isAdmin = DisableCheckBox(table)
    canWrite = DisableCheckBox(table)
    canRead = DisableCheckBox(table)
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
        isAdmin = DisableCheckBox(table)
        canWrite = DisableCheckBox(table)
        canRead = DisableCheckBox(table)
        if user in readGroup:
            canRead.setChecked(True)
        if user in writeGroup:
            canWrite.setChecked(True)
        if user in adminGroup:
            isAdmin.setChecked(True)
        if not mw.col.conf.get('pubSubName', "") in adminGroup and mw.col.conf.get('pubSubName', ""):
            isAdmin.setModifiable(False)
            canWrite.setModifiable(False)
            canRead.setModifiable(False)
            f.ui.AddUser.setEnabled(False)

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
    f.ui.Cancel.clicked.connect(lambda: f.done(0))
    f.ui.Save.clicked.connect(lambda: deckSettingsSave(table, users, did, changes, f))
    f.exec_()



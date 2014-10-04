# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deckmanager.ui'
#
# Created: Wed Sep 24 16:34:57 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AnkiPubSubDeckManager(object):
    def setupUi(self, AnkiPubSubDeckManager):
        AnkiPubSubDeckManager.setObjectName(_fromUtf8("AnkiPubSubDeckManager"))
        AnkiPubSubDeckManager.resize(506, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/Logo.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AnkiPubSubDeckManager.setWindowIcon(icon)
        self.label = QtGui.QLabel(AnkiPubSubDeckManager)
        self.label.setGeometry(QtCore.QRect(20, 10, 231, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook L"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.ankiPubSubSettings = QtGui.QPushButton(AnkiPubSubDeckManager)
        self.ankiPubSubSettings.setGeometry(QtCore.QRect(400, 10, 92, 27))
        self.ankiPubSubSettings.setObjectName(_fromUtf8("ankiPubSubSettings"))
        self.line = QtGui.QFrame(AnkiPubSubDeckManager)
        self.line.setGeometry(QtCore.QRect(-10, 40, 531, 20))
        self.line.setAutoFillBackground(False)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.newDeckGroupBox = QtGui.QGroupBox(AnkiPubSubDeckManager)
        self.newDeckGroupBox.setGeometry(QtCore.QRect(10, 340, 511, 141))
        self.newDeckGroupBox.setObjectName(_fromUtf8("newDeckGroupBox"))
        self.remoteDeckId = QtGui.QLineEdit(self.newDeckGroupBox)
        self.remoteDeckId.setGeometry(QtCore.QRect(10, 40, 381, 25))
        self.remoteDeckId.setObjectName(_fromUtf8("remoteDeckId"))
        self.readPW = QtGui.QLineEdit(self.newDeckGroupBox)
        self.readPW.setGeometry(QtCore.QRect(10, 90, 151, 25))
        self.readPW.setObjectName(_fromUtf8("readPW"))
        self.label_2 = QtGui.QLabel(self.newDeckGroupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.newDeckGroupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 171, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.newDeckGroupBox)
        self.label_4.setGeometry(QtCore.QRect(190, 70, 181, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.writePW = QtGui.QLineEdit(self.newDeckGroupBox)
        self.writePW.setGeometry(QtCore.QRect(190, 90, 201, 25))
        self.writePW.setObjectName(_fromUtf8("writePW"))
        self.ankiPubSubAddDeck = QtGui.QPushButton(self.newDeckGroupBox)
        self.ankiPubSubAddDeck.setGeometry(QtCore.QRect(410, 40, 81, 81))
        self.ankiPubSubAddDeck.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../addons/pubsub/images/Plus-Resized.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ankiPubSubAddDeck.setIcon(icon1)
        self.ankiPubSubAddDeck.setIconSize(QtCore.QSize(81, 81))
        self.ankiPubSubAddDeck.setObjectName(_fromUtf8("ankiPubSubAddDeck"))
        self.tableWidget = QtGui.QTableWidget(AnkiPubSubDeckManager)
        self.tableWidget.setGeometry(QtCore.QRect(0, 60, 501, 281))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.publishDeck = QtGui.QPushButton(AnkiPubSubDeckManager)
        self.publishDeck.setGeometry(QtCore.QRect(280, 10, 111, 27))
        self.publishDeck.setObjectName(_fromUtf8("publishDeck"))

        self.retranslateUi(AnkiPubSubDeckManager)
        QtCore.QMetaObject.connectSlotsByName(AnkiPubSubDeckManager)

    def retranslateUi(self, AnkiPubSubDeckManager):
        AnkiPubSubDeckManager.setWindowTitle(_translate("AnkiPubSubDeckManager", "AnkiPubSub Deck Manager", None))
        self.label.setText(_translate("AnkiPubSubDeckManager", "AnkiPubSub Deck Manager", None))
        self.ankiPubSubSettings.setText(_translate("AnkiPubSubDeckManager", "Settings", None))
        self.newDeckGroupBox.setTitle(_translate("AnkiPubSubDeckManager", "Subscribe to a new Deck:", None))
        self.label_2.setText(_translate("AnkiPubSubDeckManager", "Add the DeckID:", None))
        self.label_3.setText(_translate("AnkiPubSubDeckManager", "Add reading permission:", None))
        self.label_4.setText(_translate("AnkiPubSubDeckManager", "Add writing permission:", None))
        self.publishDeck.setText(_translate("AnkiPubSubDeckManager", "Publish a Deck", None))


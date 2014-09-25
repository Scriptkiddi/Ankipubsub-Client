# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_deck.ui'
#
# Created: Thu Sep 25 18:24:12 2014
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

class Ui_publishDeckForm(object):
    def setupUi(self, publishDeckForm):
        publishDeckForm.setObjectName(_fromUtf8("publishDeckForm"))
        publishDeckForm.resize(400, 300)
        self.groupBox = QtGui.QGroupBox(publishDeckForm)
        self.groupBox.setGeometry(QtCore.QRect(9, 19, 381, 71))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(0, 20, 191, 25))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(0, 0, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(200, 0, 131, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.publicName = QtGui.QLineEdit(self.groupBox)
        self.publicName.setGeometry(QtCore.QRect(200, 20, 181, 25))
        self.publicName.setObjectName(_fromUtf8("publicName"))
        self.pushButtonPublishDeck = QtGui.QPushButton(publishDeckForm)
        self.pushButtonPublishDeck.setGeometry(QtCore.QRect(30, 260, 92, 27))
        self.pushButtonPublishDeck.setObjectName(_fromUtf8("pushButtonPublishDeck"))
        self.pushButtonAbort = QtGui.QPushButton(publishDeckForm)
        self.pushButtonAbort.setGeometry(QtCore.QRect(280, 260, 92, 27))
        self.pushButtonAbort.setObjectName(_fromUtf8("pushButtonAbort"))

        self.retranslateUi(publishDeckForm)
        QtCore.QMetaObject.connectSlotsByName(publishDeckForm)

    def retranslateUi(self, publishDeckForm):
        publishDeckForm.setWindowTitle(_translate("publishDeckForm", "Publish A Deck", None))
        self.label.setText(_translate("publishDeckForm", "Select your Deck:", None))
        self.label_2.setText(_translate("publishDeckForm", "Set a Public Name:", None))
        self.pushButtonPublishDeck.setText(_translate("publishDeckForm", "Publish Deck", None))
        self.pushButtonAbort.setText(_translate("publishDeckForm", "Abort", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_deck.ui'
#
# Created: Sat Sep 27 20:53:33 2014
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
        self.publicName.setEnabled(False)
        self.publicName.setGeometry(QtCore.QRect(200, 20, 181, 25))
        self.publicName.setObjectName(_fromUtf8("publicName"))
        self.pushButtonPublishDeck = QtGui.QPushButton(publishDeckForm)
        self.pushButtonPublishDeck.setGeometry(QtCore.QRect(30, 260, 92, 27))
        self.pushButtonPublishDeck.setObjectName(_fromUtf8("pushButtonPublishDeck"))
        self.pushButtonAbort = QtGui.QPushButton(publishDeckForm)
        self.pushButtonAbort.setGeometry(QtCore.QRect(280, 260, 92, 27))
        self.pushButtonAbort.setObjectName(_fromUtf8("pushButtonAbort"))
        self.checkBox = QtGui.QCheckBox(publishDeckForm)
        self.checkBox.setGeometry(QtCore.QRect(20, 90, 271, 20))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(publishDeckForm)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 150, 311, 20))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.label_3 = QtGui.QLabel(publishDeckForm)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 121, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(publishDeckForm)
        self.label_4.setGeometry(QtCore.QRect(20, 190, 111, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit = QtGui.QLineEdit(publishDeckForm)
        self.lineEdit.setGeometry(QtCore.QRect(150, 110, 113, 25))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(publishDeckForm)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 180, 113, 25))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))

        self.retranslateUi(publishDeckForm)
        QtCore.QMetaObject.connectSlotsByName(publishDeckForm)

    def retranslateUi(self, publishDeckForm):
        publishDeckForm.setWindowTitle(_translate("publishDeckForm", "Publish A Deck", None))
        self.label.setText(_translate("publishDeckForm", "Select your Deck:", None))
        self.label_2.setText(_translate("publishDeckForm", "Set a Public Name:", None))
        self.pushButtonPublishDeck.setText(_translate("publishDeckForm", "Publish Deck", None))
        self.pushButtonAbort.setText(_translate("publishDeckForm", "Abort", None))
        self.checkBox.setText(_translate("publishDeckForm", "Users need a password to read cards.", None))
        self.checkBox_2.setText(_translate("publishDeckForm", "Users need a password to write cards", None))
        self.label_3.setText(_translate("publishDeckForm", "Reading Password:", None))
        self.label_4.setText(_translate("publishDeckForm", "Writing Password:", None))


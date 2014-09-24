# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_deck.ui'
#
# Created: Wed Sep 24 16:35:20 2014
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
        self.comboBox.setGeometry(QtCore.QRect(0, 20, 161, 25))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(0, 0, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(publishDeckForm)
        QtCore.QMetaObject.connectSlotsByName(publishDeckForm)

    def retranslateUi(self, publishDeckForm):
        publishDeckForm.setWindowTitle(_translate("publishDeckForm", "Publish A Deck", None))
        self.label.setText(_translate("publishDeckForm", "Select your Deck:", None))


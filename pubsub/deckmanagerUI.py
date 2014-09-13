# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deckmanager.ui'
#
# Created: Thu Sep 11 17:03:17 2014
#      by: PyQt4 UI code generator 4.11.1
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

class AnkiPubSubDeckManagerUI(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(506, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/Logo.jpg")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 10, 351, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook L"))
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.ankiPubSubSettings = QtGui.QPushButton(Form)
        self.ankiPubSubSettings.setGeometry(QtCore.QRect(380, 10, 92, 27))
        self.ankiPubSubSettings.setObjectName(_fromUtf8("ankiPubSubSettings"))
        self.line = QtGui.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(-10, 40, 531, 20))
        self.line.setAutoFillBackground(False)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 340, 511, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 381, 25))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 90, 151, 25))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 171, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(190, 70, 181, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(190, 90, 201, 25))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.ankiPubSubAddDeck = QtGui.QPushButton(self.groupBox)
        self.ankiPubSubAddDeck.setGeometry(QtCore.QRect(410, 40, 81, 81))
        self.ankiPubSubAddDeck.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("images/Plus-Resized.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ankiPubSubAddDeck.setIcon(icon1)
        self.ankiPubSubAddDeck.setIconSize(QtCore.QSize(81, 81))
        self.ankiPubSubAddDeck.setObjectName(_fromUtf8("ankiPubSubAddDeck"))
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(0, 60, 501, 281))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "AnkiPubSub Deck Manager", None))
        self.label.setText(_translate("Form", "AnkiPubSub Deck Manager", None))
        self.ankiPubSubSettings.setText(_translate("Form", "Settings", None))
        self.groupBox.setTitle(_translate("Form", "Subscribe to a new Deck:", None))
        self.label_2.setText(_translate("Form", "Add the DeckID:", None))
        self.label_3.setText(_translate("Form", "Add reading permission:", None))
        self.label_4.setText(_translate("Form", "Add writing permission:", None))

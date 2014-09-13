# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ankipubsub_settings.ui'
#
# Created: Sat Sep 13 12:30:20 2014
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

class AnkiPubSubSettingsUI(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(173, 169)
        self.Login = QtGui.QPushButton(Form)
        self.Login.setGeometry(QtCore.QRect(30, 120, 92, 27))
        self.Login.setObjectName(_fromUtf8("Login"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 141, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.username = QtGui.QLineEdit(Form)
        self.username.setGeometry(QtCore.QRect(20, 40, 113, 25))
        self.username.setObjectName(_fromUtf8("username"))
        self.password = QtGui.QLineEdit(Form)
        self.password.setGeometry(QtCore.QRect(20, 90, 113, 25))
        self.password.setObjectName(_fromUtf8("password"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "AnkiPubSub Settings", None))
        self.Login.setText(_translate("Form", "Login", None))
        self.label.setText(_translate("Form", "Insert your Username:", None))
        self.label_2.setText(_translate("Form", "Insert your Password:", None))
        self.username.setText(_translate("Form", "Username", None))
        self.password.setText(_translate("Form", "Password", None))


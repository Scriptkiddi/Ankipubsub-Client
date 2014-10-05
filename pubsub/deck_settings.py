# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deck_settings.ui'
#
# Created: Fri Sep 12 16:03:38 2014
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 394)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 361, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.ChecKBoxReadPassword = QtGui.QCheckBox(self.groupBox)
        self.ChecKBoxReadPassword.setGeometry(QtCore.QRect(0, 30, 271, 20))
        self.ChecKBoxReadPassword.setObjectName(_fromUtf8("ChecKBoxReadPassword"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 60, 131, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.InputReadingPassword = QtGui.QLineEdit(self.groupBox)
        self.InputReadingPassword.setGeometry(QtCore.QRect(130, 50, 113, 25))
        self.InputReadingPassword.setObjectName(_fromUtf8("InputReadingPassword"))
        self.CheckBoxWritePassword = QtGui.QCheckBox(self.groupBox)
        self.CheckBoxWritePassword.setGeometry(QtCore.QRect(0, 80, 271, 20))
        self.CheckBoxWritePassword.setObjectName(_fromUtf8("CheckBoxWritePassword"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 141, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.InputWritPassword = QtGui.QLineEdit(self.groupBox)
        self.InputWritPassword.setGeometry(QtCore.QRect(130, 110, 113, 25))
        self.InputWritPassword.setObjectName(_fromUtf8("InputWritPassword"))
        self.UserManagement = QtGui.QGroupBox(Form)
        self.UserManagement.setGeometry(QtCore.QRect(10, 150, 371, 211))
        self.UserManagement.setObjectName(_fromUtf8("UserManagement"))
        self.tableWidget = QtGui.QTableWidget(self.UserManagement)
        self.tableWidget.setGeometry(QtCore.QRect(0, 20, 371, 151))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.AddUser = QtGui.QPushButton(self.UserManagement)
        self.AddUser.setGeometry(QtCore.QRect(130, 180, 92, 27))
        self.AddUser.setObjectName(_fromUtf8("AddUser"))
        self.Cancel = QtGui.QPushButton(Form)
        self.Cancel.setGeometry(QtCore.QRect(290, 360, 92, 27))
        self.Cancel.setObjectName(_fromUtf8("Cancel"))
        self.Save = QtGui.QPushButton(Form)
        self.Save.setGeometry(QtCore.QRect(10, 360, 92, 27))
        self.Save.setObjectName(_fromUtf8("Save"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Deck Settings", None))
        self.groupBox.setTitle(_translate("Form", "Access restriction", None))
        self.ChecKBoxReadPassword.setText(_translate("Form", "Users need a password to read cards", None))
        self.label.setText(_translate("Form", "Reading Password:", None))
        self.CheckBoxWritePassword.setText(_translate("Form", "Users need a password to write cards", None))
        self.label_2.setText(_translate("Form", "Writing Password:", None))
        self.UserManagement.setTitle(_translate("Form", "User Management", None))
        self.AddUser.setText(_translate("Form", "Add User", None))
        self.Cancel.setText(_translate("Form", "Cancel", None))
        self.Save.setText(_translate("Form", "Save", None))


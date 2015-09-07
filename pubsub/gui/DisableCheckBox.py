from PyQt4 import QtGui
__author__ = 'fritz'
class DisableCheckBox(QtGui.QCheckBox):

    def __init__(self, *args, **kwargs):
        QtGui.QCheckBox.__init__(self, *args, **kwargs)
        self.is_modifiable = True
        self.clicked.connect(self.value_change_slot)

    def value_change_slot(self):
        if self.isChecked():
            self.setChecked(self.is_modifiable)
        else:
            self.setChecked(not self.is_modifiable)

    def setModifiable(self, flag):
        self.is_modifiable = flag

    def isModifiable(self):
        return self.is_modifiable
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_layer_dialog_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_SelectLayerDialog(object):
    def setupUi(self, SelectLayerDialog):
        SelectLayerDialog.setObjectName(_fromUtf8("SelectLayerDialog"))
        SelectLayerDialog.resize(339, 175)
        self.verticalLayout = QtGui.QVBoxLayout(SelectLayerDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.headerLabel = QtGui.QLabel(SelectLayerDialog)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setObjectName(_fromUtf8("headerLabel"))
        self.verticalLayout.addWidget(self.headerLabel)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.selectedLayerButton = QtGui.QRadioButton(SelectLayerDialog)
        self.selectedLayerButton.setObjectName(_fromUtf8("selectedLayerButton"))
        self.layerButtonGroup = QtGui.QButtonGroup(SelectLayerDialog)
        self.layerButtonGroup.setObjectName(_fromUtf8("layerButtonGroup"))
        self.layerButtonGroup.addButton(self.selectedLayerButton)
        self.gridLayout.addWidget(self.selectedLayerButton, 3, 0, 1, 1)
        self.newLayerButton = QtGui.QRadioButton(SelectLayerDialog)
        self.newLayerButton.setChecked(True)
        self.newLayerButton.setObjectName(_fromUtf8("newLayerButton"))
        self.layerButtonGroup.addButton(self.newLayerButton)
        self.gridLayout.addWidget(self.newLayerButton, 1, 0, 1, 2)
        self.layerComboBox = QtGui.QComboBox(SelectLayerDialog)
        self.layerComboBox.setObjectName(_fromUtf8("layerComboBox"))
        self.gridLayout.addWidget(self.layerComboBox, 3, 1, 1, 1)
        self.currentLayerButton = QtGui.QRadioButton(SelectLayerDialog)
        self.currentLayerButton.setChecked(False)
        self.currentLayerButton.setObjectName(_fromUtf8("currentLayerButton"))
        self.layerButtonGroup.addButton(self.currentLayerButton)
        self.gridLayout.addWidget(self.currentLayerButton, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(SelectLayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SelectLayerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectLayerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectLayerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectLayerDialog)

    def retranslateUi(self, SelectLayerDialog):
        SelectLayerDialog.setWindowTitle(_translate("SelectLayerDialog", "Dialog", None))
        self.headerLabel.setText(_translate("SelectLayerDialog", "Import Delimited Text Data", None))
        self.selectedLayerButton.setText(_translate("SelectLayerDialog", "Existing Point Layer", None))
        self.newLayerButton.setText(_translate("SelectLayerDialog", "Temporary Scratch Layer", None))
        self.currentLayerButton.setText(_translate("SelectLayerDialog", "Currently Selected Layer", None))


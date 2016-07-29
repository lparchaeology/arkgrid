# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_wizard_base.ui'
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

class Ui_SettingsWizard(object):
    def setupUi(self, SettingsWizard):
        SettingsWizard.setObjectName(_fromUtf8("SettingsWizard"))
        SettingsWizard.resize(668, 358)
        SettingsWizard.setOptions(QtGui.QWizard.CancelButtonOnLeft|QtGui.QWizard.NoBackButtonOnStartPage|QtGui.QWizard.NoDefaultButton)
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setObjectName(_fromUtf8("welcomePage"))
        self.gridLayout = QtGui.QGridLayout(self.welcomePage)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.welcomePage)
        self.label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        SettingsWizard.addPage(self.welcomePage)
        self.folderPage = QtGui.QWizardPage()
        self.folderPage.setObjectName(_fromUtf8("folderPage"))
        self.gridLayout_2 = QtGui.QGridLayout(self.folderPage)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.folderLabel = QtGui.QLabel(self.folderPage)
        self.folderLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.folderLabel.setWordWrap(True)
        self.folderLabel.setObjectName(_fromUtf8("folderLabel"))
        self.gridLayout_2.addWidget(self.folderLabel, 0, 0, 1, 1)
        self.projectFolderLayout = QtGui.QHBoxLayout()
        self.projectFolderLayout.setObjectName(_fromUtf8("projectFolderLayout"))
        self.projectFolderEdit = QtGui.QLineEdit(self.folderPage)
        self.projectFolderEdit.setObjectName(_fromUtf8("projectFolderEdit"))
        self.projectFolderLayout.addWidget(self.projectFolderEdit)
        self.projectFolderButton = QtGui.QToolButton(self.folderPage)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ark/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.projectFolderButton.setIcon(icon)
        self.projectFolderButton.setObjectName(_fromUtf8("projectFolderButton"))
        self.projectFolderLayout.addWidget(self.projectFolderButton)
        self.gridLayout_2.addLayout(self.projectFolderLayout, 1, 0, 1, 1)
        SettingsWizard.addPage(self.folderPage)
        self.confirmPage = QtGui.QWizardPage()
        self.confirmPage.setObjectName(_fromUtf8("confirmPage"))
        self.gridLayout_3 = QtGui.QGridLayout(self.confirmPage)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 9, 1, 1, 1)
        self.gridPointNameLabel = QtGui.QLabel(self.confirmPage)
        self.gridPointNameLabel.setObjectName(_fromUtf8("gridPointNameLabel"))
        self.gridLayout_3.addWidget(self.gridPointNameLabel, 4, 0, 1, 1)
        self.confirmLabel = QtGui.QLabel(self.confirmPage)
        self.confirmLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.confirmLabel.setWordWrap(True)
        self.confirmLabel.setObjectName(_fromUtf8("confirmLabel"))
        self.gridLayout_3.addWidget(self.confirmLabel, 0, 0, 1, 2)
        self.gridPointsNameEdit = QtGui.QLineEdit(self.confirmPage)
        self.gridPointsNameEdit.setObjectName(_fromUtf8("gridPointsNameEdit"))
        self.gridLayout_3.addWidget(self.gridPointsNameEdit, 4, 1, 1, 1)
        self.gridPolygonsNameEdit = QtGui.QLineEdit(self.confirmPage)
        self.gridPolygonsNameEdit.setEnabled(False)
        self.gridPolygonsNameEdit.setObjectName(_fromUtf8("gridPolygonsNameEdit"))
        self.gridLayout_3.addWidget(self.gridPolygonsNameEdit, 8, 1, 1, 1)
        self.gridGroupNameLabel = QtGui.QLabel(self.confirmPage)
        self.gridGroupNameLabel.setObjectName(_fromUtf8("gridGroupNameLabel"))
        self.gridLayout_3.addWidget(self.gridGroupNameLabel, 2, 0, 1, 1)
        self.gridLinesNameLabel = QtGui.QLabel(self.confirmPage)
        self.gridLinesNameLabel.setEnabled(False)
        self.gridLinesNameLabel.setObjectName(_fromUtf8("gridLinesNameLabel"))
        self.gridLayout_3.addWidget(self.gridLinesNameLabel, 6, 0, 1, 1)
        self.gridPolygonsNameLabel = QtGui.QLabel(self.confirmPage)
        self.gridPolygonsNameLabel.setEnabled(False)
        self.gridPolygonsNameLabel.setObjectName(_fromUtf8("gridPolygonsNameLabel"))
        self.gridLayout_3.addWidget(self.gridPolygonsNameLabel, 8, 0, 1, 1)
        self.gridLinesNameEdit = QtGui.QLineEdit(self.confirmPage)
        self.gridLinesNameEdit.setEnabled(False)
        self.gridLinesNameEdit.setObjectName(_fromUtf8("gridLinesNameEdit"))
        self.gridLayout_3.addWidget(self.gridLinesNameEdit, 6, 1, 1, 1)
        self.gridGroupNameEdit = QtGui.QLineEdit(self.confirmPage)
        self.gridGroupNameEdit.setObjectName(_fromUtf8("gridGroupNameEdit"))
        self.gridLayout_3.addWidget(self.gridGroupNameEdit, 2, 1, 1, 1)
        SettingsWizard.addPage(self.confirmPage)
        self.folderLabel.setBuddy(self.projectFolderEdit)
        self.gridPointNameLabel.setBuddy(self.gridPointsNameEdit)
        self.gridGroupNameLabel.setBuddy(self.gridGroupNameEdit)
        self.gridLinesNameLabel.setBuddy(self.gridLinesNameEdit)
        self.gridPolygonsNameLabel.setBuddy(self.gridPolygonsNameEdit)

        self.retranslateUi(SettingsWizard)
        QtCore.QMetaObject.connectSlotsByName(SettingsWizard)

    def retranslateUi(self, SettingsWizard):
        SettingsWizard.setWindowTitle(_translate("SettingsWizard", "Wizard", None))
        self.welcomePage.setTitle(_translate("SettingsWizard", "ARK Grid Settings Wizard", None))
        self.welcomePage.setSubTitle(_translate("SettingsWizard", "This wizard will walk you through setting up ARK Grid.", None))
        self.label.setText(_translate("SettingsWizard", "This wizard will save your settings in your project file, you must save your project otherwise this wizard will be run again. Once saved you can edit your settings by running the wizard manually.", None))
        self.folderPage.setTitle(_translate("SettingsWizard", "Project Folder", None))
        self.folderPage.setSubTitle(_translate("SettingsWizard", "Please choose your Project Folder.", None))
        self.folderLabel.setText(_translate("SettingsWizard", "This will default to your current project folder if it exists. The chosen folder will be created if it does not already exist. ARK Grid wil store the shapefiles it needs in the project folder under \'vector/grid\'.\n"
"", None))
        self.confirmPage.setTitle(_translate("SettingsWizard", "Select Files", None))
        self.confirmPage.setSubTitle(_translate("SettingsWizard", "Select the grid file names to use.", None))
        self.gridPointNameLabel.setText(_translate("SettingsWizard", "Points File Name:", None))
        self.confirmLabel.setText(_translate("SettingsWizard", "Click on the Done button to create your files. All required folders and files will be created. No existing data files will be overwritten. You must specify a Points File Name, but if you leave the Lines or Polygons field empty that file will not be created.\n"
"", None))
        self.gridGroupNameLabel.setText(_translate("SettingsWizard", "Group Name:", None))
        self.gridLinesNameLabel.setText(_translate("SettingsWizard", "Lines File Name:", None))
        self.gridPolygonsNameLabel.setText(_translate("SettingsWizard", "Polygons File Name:", None))

import resources

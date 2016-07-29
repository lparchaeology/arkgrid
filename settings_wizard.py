# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                ARK Spatial
                    A QGIS plugin for Archaeological Recording.
        Part of the Archaeological Recording Kit by L-P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2014, 2015 by L-P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2014, 2015 by John Layt
        email                : john@layt.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWizard, QFileDialog

from settings_wizard_base import *

class SettingsWizard(QWizard, Ui_SettingsWizard):

    def __init__(self, config, parent=None):
        super(SettingsWizard, self).__init__(parent)
        self._config = config
        self.setupUi(self)
        self.projectFolderButton.clicked.connect(self._selectProjectFolder)
        self.projectFolderEdit.setText(config['projectPath'])
        if config['collectionGroupName']:
            self.gridGroupNameEdit.setText(config['collectionGroupName'])
        else:
            self.gridGroupNameEdit.setText(config['groupName'])
        if config['pointsLayerName']:
            self.gridPointsNameEdit.setText(config['pointsLayerName'])
        else:
            self.gridPointsNameEdit.setText(config['pointsBaseName'])
        if config['linesLayerName']:
            self.gridLinesNameEdit.setText(config['linesLayerName'])
        else:
            self.gridLinesNameEdit.setText(config['linesBaseName'])
        if config['polygonsLayerName']:
            self.gridPolygonsNameEdit.setText(config['polygonsLayerName'])
        else:
            self.gridPolygonsNameEdit.setText(config['polygonsBaseName'])

    def config(self):
        self._config['projectPath'] = self.projectFolderEdit.text()
        self._config['collectionGroupName'] = self.gridGroupNameEdit.text()
        self._config['pointsLayerName'] = self.gridPointsNameEdit.text()
        self._config['linesLayerName'] = self.gridLinesNameEdit.text()
        self._config['polygonsLayerName'] = self.gridPolygonsNameEdit.text()
        return self._config

    def _selectProjectFolder(self):
        folderName = unicode(QFileDialog.getExistingDirectory(self, self.tr('Project Folder'), self.projectFolderEdit.text()))
        if folderName:
            self.projectFolderEdit.setText(folderName)

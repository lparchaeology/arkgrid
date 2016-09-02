# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 ARK Grid
                      A QGIS plugin for local site grids.
        Part of the Archaeological Recording Kit by L ~ P : Archaeology
                        http://ark.lparchaeology.com
                              -------------------
        begin                : 2014-12-07
        git sha              : $Format:%H$
        copyright            : 2016 by L ~ P : Heritage LLP
        email                : ark@lparchaeology.com
        copyright            : 2016 by John Layt
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

from PyQt4.QtCore import Qt, QObject, QVariant, QPoint
from PyQt4.QtGui import QApplication, QAction, QIcon, QFileDialog

from qgis.core import *
from qgis.gui import QgsVertexMarker

from libarkqgis.plugin import Plugin
from libarkqgis.layercollection import *
from libarkqgis import utils, layers
from libarkqgis.geometry import LinearTransformer
from libarkqgis.map_tools import ArkMapToolEmitPoint

from translate_features_dialog import TranslateFeaturesDialog
from select_layer_dialog import SelectLayerDialog
from update_layer_dialog import UpdateLayerDialog
from settings_wizard import SettingsWizard
from grid_wizard import GridWizard
from grid_dock import GridDock
from config import Config

import resources

class ArkGrid(Plugin):

    grid = None  # LayerCollection()

    # Internal variables
    _mapTool = None  #ArkMapToolEmitPoint()
    _initialised = False
    _gridWizard = None  # QWizard
    _vertexMarker = None  # QgsVertexMarker
    _mapTransformer = None  #LinearTransformer()
    _localTransformer = None  #LinearTransformer()

    def __init__(self, iface, pluginPath):
        super(ArkGrid, self).__init__(iface, u'ArkGrid', ':/plugins/ark/grid/icon.png', pluginPath,
                                      Plugin.PluginsGroup, Plugin.PluginsGroup, checkable=True)
        # Set display / menu name now we have tr() set up
        self.setDisplayName(self.tr(u'&ARK Grid'))

    # Standard Dock methods

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        super(ArkGrid, self).initGui()

        self.dock = GridDock()
        self.dock.initGui(self.iface, Qt.LeftDockWidgetArea, self.pluginAction)

        self._createGridAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/newGrid.png'), self.tr(u'Create New Grid'), self.showGridWizard)
        self._identifyGridAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/identifyCoordinates.png'), self.tr(u'Identify Grid Coordinates'), self._triggerMapTool)
        self._identifyGridAction.setCheckable(True)
        self._panToAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/panToSelected.svg'), self.tr(u'Pan to map point'), self.panMapToPoint)
        self._pasteMapPointAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/pastePoint.png'), self.tr(u'Paste Map Point'), self.pasteMapPointFromClipboard)
        self._addMapPointAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/addPoint.png'), self.tr(u'Add point to current layer'), self.addMapPointToLayer)
        self._updateLayerAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/updateLayer.png'), self.tr(u'Update Layer Coordinates'), self.showUpdateLayerDialog)
        self._importDelimitedAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/updateLayer.png'), self.tr(u'Import Delimited Text File'), self.showDelimitedTextDialog)
        #self._translateFeaturesAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/translateFeature.png'), self.tr(u'Translate features'), self.showTranslateFeaturesDialog)
        self._settingsWizardAction = self.dock.toolbar.addAction(QIcon(':/plugins/ark/grid/settings.svg'), self.tr(u'Run Settings Wizard'), self.configure)

        self.dock.widget.gridSelectionChanged.connect(self.changeGrid)
        self.dock.widget.mapPointChanged.connect(self.convertMapPoint)
        self.dock.widget.copyMapPointSelected.connect(self.copyMapPointToClipboard)
        self.dock.widget.localPointChanged.connect(self.convertLocalPoint)
        self.dock.widget.copyLocalPointSelected.connect(self.copyLocalPointToClipboard)

        self._setReadOnly(True)

        self._mapTool = ArkMapToolEmitPoint(self.mapCanvas())
        self._mapTool.setAction(self._identifyGridAction)
        self._mapTool.canvasClicked.connect(self.pointSelected)

        self._vertexMarker = QgsVertexMarker(self.mapCanvas())
        self._vertexMarker.setIconType(QgsVertexMarker.ICON_CROSS)

        # If the project changes make sure we stay updated
        self.iface.projectRead.connect(self.loadProject)
        self.iface.newProjectCreated.connect(self.closeProject)

    def loadProject(self):
        # Check if files exist or need creating
        # Run create if needed

        if self._initialised:
            self.closeProject();

        if self.projectPath():
            self.grid = self._loadCollection('grid', self.projectPath());
        if self.grid is None or self.grid.settings is None or self.grid.settings.pointsLayerPath == '':
            self.grid = None;
            return
        self.grid.initialise()

        if self.loadGridNames():
            self._setReadOnly(False)
            self._initialised = True
            return True
        return False

    # Save the project
    def writeProject(self):
        pass

    # Close the project
    def closeProject(self):
        if self._vertexMarker:
            self._vertexMarker.setCenter(QgsPoint())
        if self.grid is not None:
            self.grid.clearFilter()
            self.grid.unload()
            self.grid = None
        self.dock.widget.closeProject()
        self._setReadOnly(True)
        self._initialised = False

    # Unload the module when plugin is unloaded
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        del self._vertexMarker
        self._vertexMarker = None
        self._initialised = False
        self.dock.unloadGui()
        super(ArkGrid, self).unload()

    def _setReadOnly(self, readOnly):
        enabled = not readOnly
        self._identifyGridAction.setEnabled(enabled)
        self._updateLayerAction.setEnabled(enabled)
        #self._translateFeaturesAction.setEnabled(enabled)
        self._panToAction.setEnabled(enabled)
        self._pasteMapPointAction.setEnabled(enabled)
        self._addMapPointAction.setEnabled(enabled)
        self.dock.widget.setEnabled(enabled)

    def run(self, checked):
        if checked:
            if not self._initialised:
                self.loadProject()
            if self._initialised:
                self._vertexMarker.setCenter(self.mapPoint())
            else:
                self.configure()
        else:
            self._vertexMarker.setCenter(QgsPoint())

    def loadGridNames(self):
        self.grid.clearFilter()
        names = set()
        default = None
        for feature in self.grid.pointsLayer.getFeatures():
            name = (feature.attribute(Config.fieldName('site')),
                    feature.attribute(Config.fieldName('name')))
            names.add(name)
            if not default:
                default = name
        if default:
            self.setGridNames(sorted(names))
            self.setGrid(default[0], default[1])
            return True
        return False

    def initialiseGrid(self, siteCode, gridName):
        prevFilter = self.grid.filter
        expr = utils.eqClause(Config.fieldName('site'), siteCode) + ' and ' + utils.eqClause(Config.fieldName('name'), gridName)
        self.grid.applyFilter(expr)
        if self.grid.pointsLayer.featureCount() < 2:
            self.grid.applyFilter(prevFilter)
            return False
        features = []
        for feature in self.grid.pointsLayer.getFeatures():
                features.append(feature)
                if len(features) >= 2:
                    break
        map1, local1 = self.transformPoints(features[0])
        map2, local2 = self.transformPoints(features[1])
        self._mapTransformer = LinearTransformer(map1, local1, map2, local2)
        self._localTransformer = LinearTransformer(local1, map1, local2, map2)
        return True

    def changeGrid(self, siteCode, gridName):
        self.initialiseGrid(siteCode, gridName)
        self.convertMapPoint()

    def transformPoints(self, feature):
        mapPoint = feature.geometry().asPoint()
        localX = feature.attribute(Config.fieldName('local_x'))
        localY = feature.attribute(Config.fieldName('local_y'))
        localPoint = QgsPoint(localX, localY)
        return mapPoint, localPoint

    def _config(self):
        config = Config.vectorGroups['grid']
        config['projectPath'] = self.projectPath()
        lcs = None
        if self.grid and self.grid.settings:
            lcs = self.grid.settings
        else:
            lcs = LayerCollectionSettings.fromProject(self.pluginName, 'grid')
        if lcs:
            config['collectionGroupName'] = lcs.collectionGroupName
            config['pointsLayerName'] = lcs.pointsLayerName
            config['linesLayerName'] = lcs.linesLayerName
            config['polygonsLayerName'] = lcs.polygonsLayerName
        return config

    def configure(self):
        self._initialised = False
        wizard = SettingsWizard(self._config())
        if wizard.exec_():
            config = wizard.config()
            if config['projectPath'] and config['pointsLayerName'] and QDir(config['projectPath']).mkpath('.'):
                self._configureVectorGroup('grid', config)
                self.grid = self._loadCollection('grid', config['projectPath']);
                self.grid.initialise()
                self._initialised = True
        if not self._initialised:
            self.showCriticalMessage('Settings not valid, unable to continue! Please try run the wizard again.')

    def _configureVectorGroup(self, grp, config):
        path = config['pathSuffix']
        bufferPath = path + '/buffer'
        logPath = path + '/log'
        QDir(config['projectPath'] + '/' + path).mkpath('.')
        if config['buffer']:
            QDir(config['projectPath'] + '/' + bufferPath).mkpath('.')
        if config['log']:
            QDir(config['projectPath'] + '/' + logPath).mkpath('.')
        lcs = LayerCollectionSettings()
        lcs.collection = grp
        lcs.collectionPath = path
        lcs.parentGroupName = Config.projectGroupName
        lcs.collectionGroupName = config['groupName']
        lcs.bufferGroupName = config['bufferGroupName']
        lcs.log = config['log']
        if config['pointsLayerName']:
            lcs.pointsLayerLabel = config['pointsLabel']
            lcs.pointsLayerName = config['pointsLayerName']
            lcs.pointsLayerPath = self._shapeFile(path, lcs.pointsLayerName)
            lcs.pointsStylePath = self._styleFile(path, lcs.pointsLayerName, config['pointsBaseName'])
            if config['buffer']:
                lcs.pointsBufferName = lcs.pointsLayerName + Config.bufferSuffix
                lcs.pointsBufferPath = self._shapeFile(bufferPath, lcs.pointsBufferName)
            if config['log']:
                lcs.pointsLogName = lcs.pointsLayerName + Config.logSuffix
                lcs.pointsLogPath = self._shapeFile(logPath, lcs.pointsLogName)
        if config['linesLayerName']:
            lcs.linesLayerLabel = config['linesLabel']
            lcs.linesLayerName = config['linesLayerName']
            lcs.linesLayerPath = self._shapeFile(path, lcs.linesLayerName)
            lcs.linesStylePath = self._styleFile(path, lcs.linesLayerName, config['linesBaseName'])
            if config['buffer']:
                lcs.linesBufferName = lcs.linesLayerName + Config.bufferSuffix
                lcs.linesBufferPath = self._shapeFile(bufferPath, lcs.linesBufferName)
            if config['log']:
                lcs.linesLogName = lcs.linesLayerName + Config.logSuffix
                lcs.linesLogPath = self._shapeFile(logPath, lcs.linesLogName)
        if config['polygonsLayerName']:
            lcs.polygonsLayerLabel = config['polygonsLabel']
            lcs.polygonsLayerName = config['polygonsLayerName']
            lcs.polygonsLayerPath = self._shapeFile(path, lcs.polygonsLayerName)
            lcs.polygonsStylePath = self._styleFile(path, lcs.polygonsLayerName, config['polygonsBaseName'])
            if config['buffer']:
                lcs.polygonsBufferName = lcs.polygonsLayerName + Config.bufferSuffix
                lcs.polygonsBufferPath = self._shapeFile(bufferPath, lcs.polygonsBufferName)
            if config['log']:
                lcs.polygonsLogName = lcs.polygonsLayerName + Config.logSuffix
                lcs.polygonsLogPath = self._shapeFile(logPath, lcs.polygonsLogName)
        lcs.toProject('ark')
        if config['multi']:
            self._createCollectionMultiLayers(grp, lcs)
        else:
            self._createCollectionLayers(grp, lcs, config['projectPath'])

    def _loadCollection(self, collection, projectPath):
        lcs = LayerCollectionSettings.fromProject('ark', collection)
        if lcs.collection and lcs.collectionPath:
            if lcs.pointsStylePath == '':
                lcs.pointsStylePath = self._stylePath(lcs.collection, lcs.collectionPath, lcs.pointsLayerName, 'pointsBaseName')
            if lcs.linesStylePath == '':
                lcs.linesStylePath = self._stylePath(lcs.collection, lcs.collectionPath, lcs.linesLayerName, 'linesBaseName')
            if lcs.polygonsStylePath == '':
                lcs.polygonsStylePath = self._stylePath(lcs.collection, lcs.collectionPath, lcs.polygonsLayerName, 'polygonsBaseName')
        return LayerCollection(self.iface, projectPath, lcs)

    def _createCollectionLayers(self, collection, settings, projectPath):
        if (settings.pointsLayerPath and not QFile.exists(projectPath + '/' + settings.pointsLayerPath)):
            layers.createShapefile(projectPath + '/' + settings.pointsLayerPath,   settings.pointsLayerName,   QGis.WKBPoint,
                                   self.projectCrs(), self._layerFields(collection, 'pointsFields'))
        if (settings.linesLayerPath and not QFile.exists(projectPath + '/' + settings.linesLayerPath)):
            layers.createShapefile(projectPath + '/' + settings.linesLayerPath,    settings.linesLayerName,    QGis.WKBLineString,
                                   self.projectCrs(), self._layerFields(collection, 'linesFields'))
        if (settings.polygonsLayerPath and not QFile.exists(projectPath + '/' + settings.polygonsLayerPath)):
            layers.createShapefile(projectPath + '/' + settings.polygonsLayerPath, settings.polygonsLayerName, QGis.WKBPolygon,
                                   self.projectCrs(), self._layerFields(collection, 'polygonsFields'))

    def _layerFields(self, collection, fieldsKey):
        fieldKeys = Config.vectorGroups[collection][fieldsKey]
        fields = QgsFields()
        for fieldKey in fieldKeys:
            fields.append(Config.fieldDefaults[fieldKey])
        return fields

    def _shapeFile(self, layerPath, layerName):
        return layerPath + '/' + layerName + '.shp'

    def _stylePath(self, collection, collectionPath, layerName, baseName):
        return self._styleFile(collectionPath, layerName, Config.vectorGroups[collection][baseName])

    def _styleFile(self, layerPath, layerName, baseName):
        # First see if the layer itself has a default style saved
        filePath = layerPath + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the layer name has a style in the styles folder (which may be a special folder, the site folder or the plugin folder)
        filePath = self.stylePath() + '/' + layerName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Next see if the default name has a style in the style folder
        filePath = self.stylePath() + '/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # Finally, check the plugin folder for the default style
        filePath = self.pluginPath() + '/styles/' + baseName + '.qml'
        if QFile.exists(filePath):
            return filePath
        # If we didn't find that then something is wrong!
        return ''

    def projectPath(self):
        return QgsProject.instance().homePath()

    def stylePath(self):
        path =  self.readEntry('stylePath', '')
        if (not path):
            return self.pluginPath + '/styles'
        return path

    # Widget settings methods

    def siteCode(self):
        return self.dock.widget.siteCode()

    def gridName(self):
        return self.dock.widget.gridName()

    def setGrid(self, siteCode, gridName):
        self.dock.widget.setGrid(siteCode, gridName)

    def setGridNames(self, names):
        self.dock.widget.setGridNames(names)

    def mapPoint(self):
        return self.dock.widget.mapPoint()

    def setMapPoint(self, point):
        self.dock.widget.setMapPoint(point)
        self._vertexMarker.setCenter(self.mapPoint())

    def localPoint(self):
        return self.dock.widget.localPoint()

    def setLocalPoint(self, point):
        self.dock.widget.setLocalPoint(point)

    # Grid methods

    def showGridWizard(self):
        if self._gridWizard is None:
            self._gridWizard = GridWizard(self.iface, self, self.iface.mainWindow())
            self._gridWizard.accepted.connect(self.createGridDialogAccepted)
        else:
            self._gridWizard.restart()
        self._gridWizard.show()
        self._gridWizard._showDialog()

    def createGridDialogAccepted(self):
        mp1 = self._gridWizard.mapPoint1()
        lp1 = self._gridWizard.localPoint1()
        mp2 = self._gridWizard.mapPoint2()
        lp2 = self._gridWizard.localPoint2()
        xInterval = self._gridWizard.localEastingInterval()
        yInterval = self._gridWizard.localNorthingInterval()
        if self._gridWizard.methodType() != GridWizard.TwoKnownPoints:
            axisGeometry = QgsGeometry.fromPolyline([mp1, mp2])
            mapAxisPoint = None
            localAxisPoint = None
            if self._gridWizard.methodType() == GridWizard.PointOnYAxis:
                if axisGeometry.length() < yInterval:
                    self.showCriticalMessage('Cannot create grid: Input axis must be longer than local interval')
                    return False
                mp2 = axisGeometry.interpolate(yInterval).asPoint()
                lp2 = QgsPoint(lp1.x(), lp1.y() + yInterval)
            else:
                if axisGeometry.length() < xInterval:
                    self.showCriticalMessage('Cannot create grid: Input axis must be longer than local interval')
                    return False
                mp2 = axisGeometry.interpolate(xInterval).asPoint()
                lp2 = QgsPoint(lp1.x() + xInterval, lp1.y())
        if self.createGrid(self._gridWizard.siteCode(), self._gridWizard.gridName(),
                           mp1, lp1, mp2, lp2,
                           self._gridWizard.localOriginPoint(), self._gridWizard.localTerminusPoint(),
                           xInterval, yInterval):
            self.mapCanvas().refresh()
            self.loadGridNames()
            self.setGrid(self._gridWizard.siteCode(), self._gridWizard.gridName())
            self._setReadOnly(False)
            self.showInfoMessage('Grid successfully created', 10)

    def createGrid(self, siteCode, gridName, mapPoint1, localPoint1, mapPoint2, localPoint2, localOrigin, localTerminus, xInterval, yInterval):
        _localTransformer = LinearTransformer(localPoint1, mapPoint1, localPoint2, mapPoint2)
        local_x = Config.fieldName('local_x')
        local_y = Config.fieldName('local_y')
        map_x = Config.fieldName('map_x')
        map_y = Config.fieldName('map_y')

        points = self.grid.pointsLayer
        if (points is None or not points.isValid()):
            self.showCriticalMessage('Invalid grid points file, cannot create grid!')
            return False
        self._addGridPointsToLayer(points, _localTransformer,
                                   localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                   localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                   self._attributes(points, siteCode, gridName), local_x, local_y, map_x, map_y)

        if self.grid.settings.linesLayerName:
            lines = self.grid.linesLayer
            if lines is None or not lines.isValid():
                self.showCriticalMessage('Invalid grid lines file!')
            else:
                self._addGridLinesToLayer(lines, _localTransformer,
                                          localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                          localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                          self._attributes(lines, siteCode, gridName), local_x, local_y, map_x, map_y)

        if self.grid.settings.polygonsLayerName:
            polygons = self.grid.polygonsLayer
            if lines is None or not lines.isValid():
                self.showCriticalMessage('Invalid grid polygons file!')
            else:
                self._addGridPolygonsToLayer(polygons, _localTransformer,
                                             localOrigin.x(), xInterval, (localTerminus.x() - localOrigin.x()) / xInterval,
                                             localOrigin.y(), yInterval, (localTerminus.y() - localOrigin.y()) / yInterval,
                                             self._attributes(polygons, siteCode, gridName), local_x, local_y, map_x, map_y)
        return True

    def _attributes(self, layer, site, name):
        attributes = {}
        attributes[layer.fieldNameIndex(Config.fieldName('site'))] = site
        attributes[layer.fieldNameIndex(Config.fieldName('name'))] = name
        attributes[layer.fieldNameIndex(Config.fieldName('created_on'))] = utils.timestamp()
        attributes[layer.fieldNameIndex(Config.fieldName('created_by'))] = 'Grid Tool'
        return attributes

    def _setAttributes(self, feature, attributes):
        for key in attributes.keys():
            feature.setAttribute(key, attributes[key])

    def _addGridPointsToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Point):
            return
        features = []
        for localX in range(originX, originX + (intervalX * repeatX) + 1, intervalX):
            for localY in range(originY, originY + (intervalY * repeatY) + 1, intervalY):
                localPoint = QgsPoint(localX, localY)
                mapPoint = transformer.map(localPoint)
                feature = QgsFeature(layer.dataProvider().fields())
                feature.setGeometry(QgsGeometry.fromPoint(mapPoint))
                self._setAttributes(feature, attributes)
                feature.setAttribute(localFieldX, localX)
                feature.setAttribute(localFieldY, localY)
                feature.setAttribute(mapFieldX, mapPoint.x())
                feature.setAttribute(mapFieldY, mapPoint.y())
                features.append(feature)
        layers.addFeatures(features, layer)

    def _addGridLinesToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Line):
            return
        features = []
        terminusX = originX + (intervalX * repeatX)
        terminusY = originY + (intervalY * repeatY)
        for localX in range(originX, originX + (intervalX * repeatX) + 1, intervalX):
            localStartPoint = QgsPoint(localX, originY)
            localEndPoint = QgsPoint(localX, terminusY)
            mapStartPoint = transformer.map(localStartPoint)
            mapEndPoint = transformer.map(localEndPoint)
            feature = QgsFeature(layer.dataProvider().fields())
            feature.setGeometry(QgsGeometry.fromPolyline([mapStartPoint, mapEndPoint]))
            self._setAttributes(feature, attributes)
            feature.setAttribute(localFieldX, localX)
            feature.setAttribute(mapFieldX, mapStartPoint.x())
            features.append(feature)
        for localY in range(originY, originY + (intervalY * repeatY) + 1, intervalY):
            localStartPoint = QgsPoint(originX, localY)
            localEndPoint = QgsPoint(terminusX, localY)
            mapStartPoint = transformer.map(localStartPoint)
            mapEndPoint = transformer.map(localEndPoint)
            feature = QgsFeature(layer.dataProvider().fields())
            feature.setGeometry(QgsGeometry.fromPolyline([mapStartPoint, mapEndPoint]))
            self._setAttributes(feature, attributes)
            feature.setAttribute(localFieldY, localY)
            feature.setAttribute(mapFieldY, mapStartPoint.y())
            features.append(feature)
        layers.addFeatures(features, layer)

    def _addGridPolygonsToLayer(self, layer, transformer, originX, intervalX, repeatX, originY, intervalY, repeatY, attributes, localFieldX='local_x', localFieldY='local_x', mapFieldX='map_x', mapFieldY='map_y'):
        if (layer is None or not layer.isValid() or layer.geometryType() != QGis.Polygon):
            return
        features = []
        for localX in range(originX, originX + intervalX * repeatX, intervalX):
            for localY in range(originY, originY + intervalY * repeatY, intervalY):
                localPoint = QgsPoint(localX, localY)
                mapPoint = transformer.map(localPoint)
                points = []
                points.append(transformer.map(localPoint))
                points.append(transformer.map(QgsPoint(localX, localY + intervalY)))
                points.append(transformer.map(QgsPoint(localX + intervalX, localY + intervalY)))
                points.append(transformer.map(QgsPoint(localX + intervalX, localY)))
                feature = QgsFeature(layer.dataProvider().fields())
                feature.setGeometry(QgsGeometry.fromPolygon([points]))
                self._setAttributes(feature, attributes)
                feature.setAttribute(localFieldX, localX)
                feature.setAttribute(localFieldY, localY)
                feature.setAttribute(mapFieldX, mapPoint.x())
                feature.setAttribute(mapFieldY, mapPoint.y())
                features.append(feature)
        layers.addFeatures(features, layer)

    def _triggerMapTool(self):
        if self._initialised:
            if self._identifyGridAction.isChecked():
                self.mapCanvas().setMapTool(self._mapTool)
            else:
                self.mapCanvas().unsetMapTool(self._mapTool)
        elif self._identifyGridAction.isChecked():
            self._identifyGridAction.setChecked(False)

    def pointSelected(self, point, button):
        if not self._initialised:
            return
        if (button == Qt.LeftButton):
            if not self.dock.menuAction().isChecked():
                self.dock.menuAction().toggle()
            self.setMapPoint(point)
            self.convertMapPoint()

    def convertMapPoint(self):
        if not self._initialised:
            return
        localPoint = self._mapTransformer.map(self.mapPoint())
        self.setLocalPoint(localPoint)

    def convertLocalPoint(self):
        if not self._initialised:
            return
        mapPoint = self._localTransformer.map(self.localPoint())
        self.setMapPoint(mapPoint)

    def showUpdateLayerDialog(self):
        if self._initialised:
            dialog = UpdateLayerDialog(self.iface)
            if dialog.exec_():
                self.updateLayerCoordinates(dialog.layer(), dialog.updateGeometry(), dialog.createMapFields())

    def _addField(self, layer, field):
        if layer.fieldNameIndex(Config.fieldName(field)) < 0:
            layer.dataProvider().addAttributes([Config.field(field)])

    def _addLocalMapFields(self, layer, createMapFields):
        self._addField(layer, 'local_x')
        self._addField(layer, 'local_y')
        if (createMapFields):
            self._addField(layer, 'map_x')
            self._addField(layer, 'map_y')

    def updateLayerCoordinates(self, layer, updateGeometry, createMapFields):
        if (not self._initialised or layer is None or not layer.isValid() or layer.geometryType() != QGis.Point):
            return False
        self._addLocalMapFields(layer, createMapFields)
        if layer.startEditing():
            local_x_idx = layer.fieldNameIndex(Config.fieldName('local_x'))
            local_y_idx = layer.fieldNameIndex(Config.fieldName('local_y'))
            map_x_idx = layer.fieldNameIndex(Config.fieldName('map_x'))
            map_y_idx = layer.fieldNameIndex(Config.fieldName('map_y'))
            if updateGeometry:
                for feature in layer.getFeatures():
                    localPoint = QgsPoint(feature.attribute(Config.fieldName('local_x')), feature.attribute(Config.fieldName('local_y')))
                    mapPoint = self._localTransformer.map(localPoint)
                    layer.changeGeometry(feature.id(), QgsGeometry.fromPoint(mapPoint))
            for feature in layer.getFeatures():
                mapPoint = feature.geometry().asPoint()
                localPoint = self._mapTransformer.map(mapPoint)
                layer.changeAttributeValue(feature.id(), local_x_idx, localPoint.x())
                layer.changeAttributeValue(feature.id(), local_y_idx, localPoint.y())
                layer.changeAttributeValue(feature.id(), map_x_idx, mapPoint.x())
                layer.changeAttributeValue(feature.id(), map_y_idx, mapPoint.y())
            return layer.commitChanges()
        return False

    def showTranslateFeaturesDialog(self):
        if self._initialised:
            dialog = TranslateFeaturesDialog(self.iface)
            if dialog.exec_():
                self.translateFeatures(dialog.layer(), dialog.translateEast(), dialog.translateNorth(), dialog.allFeatures())

    def translateFeatures(self, layer, xInterval, yInterval, allFeatures):
        localOriginPoint = QgsPoint(0, 0)
        localTranslatedPoint = QgsPoint(xInterval, yInterval)
        mapOriginPoint = self._localTransformer.map(localOriginPoint)
        mapTranslatedPoint = self._localTransformer.map(localTranslatedPoint)
        dx = mapTranslatedPoint.x() - mapOriginPoint.x()
        dy = mapTranslatedPoint.y() - mapOriginPoint.y()
        if layer.startEditing():
            featureIds = None
            if allFeatures:
                featureIds = layer.allFeatureIds()
            else:
                featureIds = layer.selectedFeaturesIds()
            for featureId in featureIds:
                layer.translateFeature(featureId, dx, dy)
            if layer.commitChanges():
                return self.updateLayerCoordinates(layer, False, False)
        return False

    def panMapToPoint(self):
        self.mapCanvas().zoomByFactor(1.0, self.mapPoint())

    def copyMapPointToClipboard(self):
        #TODO Use QgsClipboard when it becomes public
        QApplication.clipboard().setText(self.mapPointAsWkt())

    def copyLocalPointToClipboard(self):
        #TODO Use QgsClipboard when it becomes public
        QApplication.clipboard().setText(self.localPointAsWkt())

    def pasteMapPointFromClipboard(self):
        #TODO Use QgsClipboard when it becomes public
        text = QApplication.clipboard().text().strip().upper()
        idx = text.find('POINT(')
        if idx >= 0:
            idx_l = idx + 5
            idx_r = text.find(')', idx_l) + 1
            text = text[idx_l:idx_r]
        if (text[0] == '(' and text[len(text) - 1] == ')'):
            coords = text[1:len(text) - 2].split()
            point = QgsPoint(float(coords[0]), float(coords[1]))
            self.setMapPoint(point)

    def addMapPointToLayer(self):
        layer = self.mapCanvas().currentLayer()
        if (layer.geometryType() == QGis.Point and layer.isEditable()):
            layer.addFeature(self.mapPointAsFeature(layer.pendingFields()))
        self.mapCanvas().refresh()

    def setMapPointFromGeometry(self, geom):
        if (geom is not None and geom.type() == QGis.Point and geom.isGeosValid()):
            self.setMapPoint(geom.asPoint())

    def setMapPointFromWkt(self, wkt):
        self.setMapPointFromGeometry(QgsGeometry.fromWkt(wkt))

    def mapPointAsGeometry(self):
        return QgsGeometry.fromPoint(self.mapPoint())

    def mapPointAsFeature(self, fields):
        feature = QgsFeature(fields)
        feature.setGeometry(self.mapPointAsGeometry())
        return feature

    def mapPointAsLayer(self):
        mem = QgsVectorLayer("point?crs=" + self.projectCrs().authid() + "&index=yes", 'point', 'memory')
        if (mem is not None and mem.isValid()):
            mem.dataProvider().addAttributes([QgsField('id', QVariant.String, '', 10, 0, 'ID')])
            feature = self.mapPointAsFeature(mem.dataProvider().fields())
            mem.dataProvider().addFeatures([feature])
        return mem

    def mapPointAsWkt(self):
        # Return the text so we don't have insignificant double values
        return 'POINT(' + self.dock.widget.mapEastingSpin.text() + ' ' + self.dock.widget.mapNorthingSpin.text() + ')'

    def setLocalPointFromGeometry(self, geom):
        if (geom is not None and geom.type() == QGis.Point and geom.isGeosValid()):
            self.setLocalPoint(geom.asPoint())

    def setLocalPointFromWkt(self, wkt):
        self.setLocalPointFromGeometry(QgsGeometry.fromWkt(wkt))

    def localPointAsGeometry(self):
        return QgsGeometry.fromPoint(self.localPoint())

    def localPointAsWkt(self):
        # Return the text so we don't have insignificant double values
        return 'POINT(' + self.dock.widget.localEastingSpin.text() + ' ' + self.dock.widget.localNorthingSpin.text() + ')'

    def showDelimitedTextDialog(self):
        # HACK to access private dialog!!!
        dialog = QgsProviderRegistry.instance().selectWidget("delimitedtext", self.iface.mainWindow())
        dialog.addVectorLayer.connect(self.loadDelimitedText)
        dialog.show()

    def loadDelimitedText(self, url, layerName, provider):
        #unload the layer

        inLayer = QgsVectorLayer(url, 'temp', provider)
        if (inLayer is None or not inLayer.isValid()):
            return

        dialog = SelectLayerDialog(self.iface)
        toLayer = None
        if dialog.exec_():
            if dialog.currentLayer():
                toLayer = self.mapCanvas().currentLayer()
            elif dialog.selectedLayer():
                toLayer = dialog.layer()
            elif dialog.newLayer():
                fields = inLayer.pendingFields()
                toLayer = layers.createMemoryLayer(layerName, QGis.WKBPoint, self.projectCrs(), fields)
                layers.addLayerToLegend(self.iface, toLayer)

        if toLayer and toLayer.geometryType() == QGis.Point:
            self._addLocalMapFields(toLayer, False)
            if toLayer.startEditing():
                for feature in inLayer.getFeatures():
                    toLayer.addFeature(feature)

        self.mapCanvas().refresh()

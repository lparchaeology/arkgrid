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

from PyQt4.QtCore import QVariant

from qgis.core import QgsField

class Config():

    @classmethod
    def fields(cls):
        return cls.fieldDefaults

    @classmethod
    def field(cls, fieldKey):
        return cls.fieldDefaults[fieldKey]

    @classmethod
    def fieldName(cls, fieldKey):
        try:
            return cls.fieldDefaults[fieldKey].name()
        except:
            return ''

    pluginName = u'ArkGrid'
    projectGroupName = u'Ark Grid'
    bufferSuffix = '_buf'
    logSuffix = '_log'

    # Field deafults to use if *not* using ARK DB, so as not to confuse normal users
    fieldDefaults = {
        'site'      : QgsField('site',       QVariant.String, '',  10, 0, 'Site Code'),
        'name'      : QgsField('name',       QVariant.String, '',  10, 0, 'Name'),
        'local_x'   : QgsField('local_x',    QVariant.Double, '',  10, 3, 'Local Grid X'),
        'local_y'   : QgsField('local_y',    QVariant.Double, '',  10, 3, 'Local Grid Y'),
        'map_x'     : QgsField('map_x',      QVariant.Double, '',  10, 3, 'Map X'),
        'map_y'     : QgsField('map_y',      QVariant.Double, '',  10, 3, 'Map Y'),
        'created_on': QgsField('created_on', QVariant.String, '',  20, 0, 'Created On'),  # '2012-01-01T23:59:59.999Z' in UTC
        'created_by': QgsField('created_by', QVariant.String, '',  20, 0, 'Created By'),
    }

    vectorGroups = {
        'grid' : {
            'pathSuffix'       : 'vector/grid',
            'groupName'        : 'Grid Data',
            'buffer'           : False,
            'bufferGroupName'  : '',
            'log'              : False,
            'multi'            : False,
            'pointsLabel'      : 'Grid Points',
            'linesLabel'       : 'Grid Lines',
            'polygonsLabel'    : 'Grid Polygons',
            'pointsBaseName'   : 'grid_pt',
            'linesBaseName'    : 'grid_pl',
            'polygonsBaseName' : 'grid_pg',
            'pointsFields'     : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
            'linesFields'      : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
            'polygonsFields'   : ['site', 'name', 'local_x', 'local_y', 'map_x', 'map_y', 'created_on', 'created_by'],
        },
    }

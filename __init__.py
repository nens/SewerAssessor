# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SewerAssessor
                                 A QGIS plugin
 De Sewer Assessor is een QGIS plug-in die helpt bij het bepalen van eigenschappen van de riolering.
                             -------------------
        begin                : 2017-04-26
        copyright            : (C) 2017 by Nelen & Schuurmans
        email                : madeleine.vanwinkel@nelen-schuurmans.nl
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SewerAssessor class from file SewerAssessor.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .sewer_assessor import SewerAssessor
    return SewerAssessor(iface)

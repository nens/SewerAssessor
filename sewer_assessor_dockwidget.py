# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SewerAssessorDockWidget
                                 A QGIS plugin
 De Sewer Assessor is een QGIS plug-in die helpt bij het bepalen van eigenschappen van de riolering.
                             -------------------
        begin                : 2017-04-26
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Nelen & Schuurmans
        email                : madeleine.vanwinkel@nelen-schuurmans.nl
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

from .utils.constants import TEXTBOX_R_I_GEBIEDSGRENZEN
from .utils.constants import TEXTBOX_R_I_GEM_ZETTINGSSNELHEID_PUT
from .utils.constants import TEXTBOX_R_I_RIOOLPUTTEN
from .utils.constants import TEXTBOX_R_I_RIOOLLEIDINGEN
from .utils.constants import TEXTBOX_R_I_AHN

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'sewer_assessor_dockwidget_base.ui'))


class SewerAssessorDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(SewerAssessorDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def set_filename(self, TEXTBOX, filename):
        """Set the filename in the proper textbox."""
        if TEXTBOX == TEXTBOX_R_I_GEBIEDSGRENZEN:
            self.r_i_gebiedsgrenzen_text.setText(filename)
        if TEXTBOX == TEXTBOX_R_I_GEM_ZETTINGSSNELHEID_PUT:
            self.r_i_gem_zettingssnelheid_put_text.setText(filename)
        if TEXTBOX == TEXTBOX_R_I_RIOOLPUTTEN:
            self.r_i_rioolputten_text.setText(filename)
        if TEXTBOX == TEXTBOX_R_I_RIOOLLEIDINGEN:
            self.r_i_rioolleidingen_text.setText(filename)
        if TEXTBOX == TEXTBOX_R_I_AHN:
            self.r_i_ahn_text.setText(filename)

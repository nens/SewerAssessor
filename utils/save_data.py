# # -*- coding: utf-8 -*-
# """Module for getting data from files."""
import os.path

from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QSettings
# from PyQt4.QtGui import QFileDialog


def save_shape(self):
    """Function to get a file."""
    settings = QSettings('sewer_assessor', 'qgisplugin')

    try:
        init_path = settings.value('last_used_import_path', type=str)
    except TypeError:
        init_path = os.path.expanduser("~")
    filename = QFileDialog.getSaveFileName(None,
                                           'Save shapefile',
                                           init_path,
                                           'ESRI shapefile (*.shp)')
    return filename

# # -*- coding: utf-8 -*-
# """Module for getting data from files."""
import os.path

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QFileDialog


def get_file(self):
    """Function to get a file."""
    settings = QSettings('sewer_assessor', 'qgisplugin')

    try:
        init_path = settings.value('last_used_import_path', type=str)
    except TypeError:
        init_path = os.path.expanduser("~")
    filename = QFileDialog.getOpenFileName(None,
                                           'Select import file',
                                           init_path,
                                           'ESRI shapefile (*.shp)')

    if filename:
        settings.setValue('last_used_import_path',
                          os.path.dirname(filename))
    return filename

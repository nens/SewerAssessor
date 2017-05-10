# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SewerAssessor
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
import os.path
import processing
import re

from qgis.core import QgsField
from qgis.core import QgsVectorFileWriter
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import qVersion
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon
# Initialize Qt resources from file resources.py
import resources

# Import the code for the DockWidget
from .sewer_assessor_dockwidget import SewerAssessorDockWidget
from .utils.constants import BUTTON_R_I_GEBIEDSGRENZEN
from .utils.constants import TEXTBOX_R_I_GEBIEDSGRENZEN
from .utils.constants import BUTTON_R_I_GEM_ZETTINGSSNELHEID_PUT
from .utils.constants import TEXTBOX_R_I_GEM_ZETTINGSSNELHEID_PUT
from .utils.constants import BUTTON_R_I_RIOOLPUTTEN
from .utils.constants import TEXTBOX_R_I_RIOOLPUTTEN
from .utils.constants import BUTTON_R_I_RIOOLLEIDINGEN
from .utils.constants import TEXTBOX_R_I_RIOOLLEIDINGEN
from .utils.constants import BUTTON_R_I_AHN
from .utils.constants import TEXTBOX_R_I_AHN
from .utils.get_data import get_file
from .utils.save_data import save_shape
from .utils.layer import add_label_to_layer
from .utils.layer import add_layer


class SewerAssessor:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SewerAssessor_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Sewer Assessor')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SewerAssessor')
        self.toolbar.setObjectName(u'SewerAssessor')

        # print "** INITIALIZING SewerAssessor"

        self.pluginIsActive = False
        self.dockwidget = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SewerAssessor', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/SewerAssessor/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Sewer Assessor'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        # print "** CLOSING SewerAssessor"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Remove the plugin menu item and icon from QGIS GUI."""
        # print "** UNLOAD SewerAssessor"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Sewer Assessor'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that loads and starts the plugin."""
        if not self.pluginIsActive:
            self.pluginIsActive = True

            # print "** STARTING SewerAssessor"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = SewerAssessorDockWidget()
                # INPUT
                # Connect the search buttons with the search_file functions
                self.dockwidget.r_i_gebiedsgrenzen_search.clicked.connect(
                    self.search_file_r_i_gebiedsgrenzen)
                self.dockwidget.r_i_gem_zettingssnelheid_put_search.clicked.connect(
                    self.search_file_r_i_gem_zettingssnelheid_put_search)
                self.dockwidget.r_i_rioolputten_search.clicked.connect(
                    self.search_file_r_i_rioolputten_search)
                self.dockwidget.r_i_rioolleidingen_search.clicked.connect(
                    self.search_file_r_i_rioolleidingen_search)
                self.dockwidget.r_i_ahn_search.clicked.connect(
                    self.search_file_r_i_ahn)
                # OUTPUT
                # Connect gem zettingssnelheid put to gem_zettingssnelheid_put
                # function
                self.dockwidget.r_o_gem_zettingssnelheid_put_button.clicked.connect(
                    self.gem_zettingssnelheid_put)
                # Connect gem zettingssnelheid put to gem_zettingssnelheid_put
                # function
                self.dockwidget.r_o_gem_zettingssnelheid_rioolgebied_button.clicked.connect(
                    self.gem_zettingssnelheid_rioolgebied)
                # Connect absolute zetting put to abs_zetting_put function
                self.dockwidget.r_o_abs_zetting_put_button.clicked.connect(
                    self.abs_zetting_put)
                # Connect gem abs zetting rioolgebied to gem_abs_zet_rioolgebied function
                self.dockwidget.r_o_gem_abs_zetting_rioolgebied_button.clicked.connect(
                    self.gem_abs_zet_rioolgebied)
                # Connect gem jaar aanleg rioolgebied to gem_jaar_aanleg_rioolgebied function
                self.dockwidget.r_o_gem_jaar_aanleg_rioolgebied_button.clicked.connect(
                    self.gem_jaar_aanleg_rioolgebied)
                # Connect gem jaar aanleg rioolgebied to gem_jaar_aanleg_rioolgebied function
                self.dockwidget.r_o_jaar_van_falen_rioolgebied_button.clicked.connect(
                    self.jaar_van_falen_rioolgebied)

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

    def search_file_r_i_gebiedsgrenzen(self):
        """Get the input file of 'Gebiedsgrenzen'."""
        self.search_file(BUTTON_R_I_GEBIEDSGRENZEN)

    def search_file_r_i_gem_zettingssnelheid_put_search(self):
        """Get the input file of 'Gem. zettingssnelheid put'."""
        self.search_file(BUTTON_R_I_GEM_ZETTINGSSNELHEID_PUT)

    def search_file_r_i_rioolputten_search(self):
        """Get the input file of 'Riool putten'."""
        self.search_file(BUTTON_R_I_RIOOLPUTTEN)

    def search_file_r_i_rioolleidingen_search(self):
        """Get the input file of 'Riool leidingen'."""
        self.search_file(BUTTON_R_I_RIOOLLEIDINGEN)

    def search_file_r_i_ahn(self):
        """Get the input file of 'Actueel Hoogtebestand NL'."""
        self.search_file(BUTTON_R_I_AHN)

    def search_file(self, BUTTON):
        """Function to search a file."""
        if BUTTON == BUTTON_R_I_GEBIEDSGRENZEN:
            textbox = TEXTBOX_R_I_GEBIEDSGRENZEN
        if BUTTON == BUTTON_R_I_GEM_ZETTINGSSNELHEID_PUT:
            textbox = TEXTBOX_R_I_GEM_ZETTINGSSNELHEID_PUT
        if BUTTON == BUTTON_R_I_RIOOLPUTTEN:
            textbox = TEXTBOX_R_I_RIOOLPUTTEN
        if BUTTON == BUTTON_R_I_RIOOLLEIDINGEN:
            textbox = TEXTBOX_R_I_RIOOLLEIDINGEN
        if BUTTON == BUTTON_R_I_AHN:
            textbox = TEXTBOX_R_I_AHN
        filename = get_file(self)
        self.dockwidget.set_filename(textbox, filename)
        # if BUTTON == BUTTON_R_I_GEBIEDSGRENZEN:
        #     set_attributes_in_combobox(combobox, attributes)

    def gem_zettingssnelheid_put(self):
        """Bereken en toon gemiddelde zettingssnelheid per put."""
        # 1. Laad shapefile in met putdata (putten_export_kikker.shp)
        self.layer_rioolputten = self.iface.addVectorLayer(
            self.dockwidget.r_i_rioolputten_text.text(),
            "putten_export_kikker",
            "ogr")
        # 2. Laad shapefile in met putcodes en zettingssnelheden
        # (putten_stats.shp)
        self.layer_gem_zettingssnelheid_put = self.iface.addVectorLayer(
            self.dockwidget.r_i_gem_zettingssnelheid_put_text.text(),
            "putten_stats",
            "ogr")
        # 3. Create a new shapefile with the features of the putdata
        # (putten_export_kikker.shp)
        save_message = "Save gemiddelde zettingssnelheid rioolput"
        output = save_shape(self, save_message)
        output_name = "{}.shp".format(output)
        # 4. Join putdata(Knoopnr) with the putten of putten_stats.shp
        # (putcode)
        target_field = "Knoopnr"
        input_field = "putcode"
        self.layer_rioolputten_joined = processing.runalg(
            'qgis:joinattributestable', self.layer_rioolputten,
            self.layer_gem_zettingssnelheid_put, target_field, input_field,
            output)
        # Add the layer to the map
        self.layer_rioolputten_joined = add_layer(self.iface, output_name)

    def gem_zettingssnelheid_rioolgebied(self):
        """Toon gemiddelde zettingssnelheid per rioolgebied."""
        # 1. Laad shapefile in met gebiedsgrenzen (putten_export_kikker.shp)
        self.layer_gebiedsgrenzen = self.iface.addVectorLayer(
            self.dockwidget.r_i_gebiedsgrenzen_text.text(),
            "gebiedsgrenzen",
            "ogr")
        # 2. Referentie naar de putdata --> self.layer_rioolputten
        # 3. Aggregeer putdata naar de gebiedsgrenzen
        save_message = "Save gemiddelde zettingssnelheid rioolgebied"
        self.layer_aggregeer_putten = self.aggregeer_putten(
            self.layer_gebiedsgrenzen, self.layer_rioolputten, save_message)
        # Rename field to mean zettingssnelheid
        # # Spatial index maakt dit sneller!

    def aggregeer_putten(self, polygons, points, save_message):
        """Aggregeer de putten naar de rioolgebieden."""
        # Create join_layers_by_location function in layers module
        output = save_shape(self, save_message)
        output_name = "{}.shp".format(output)
        processing.runalg(
            "qgis:joinattributesbylocation", polygons, points, u'contains', 1,
            0, u'mean', 0, output)

        # Add the layer to the map
        layer_name = re.sub(r".*/", "", output_name)
        layer_name = re.sub(r".shp", "", layer_name)
        layer = self.iface.addVectorLayer(output_name, layer_name, "ogr")
        return layer

    def abs_zetting_put(self):
        """Calculate the absolute zetting of the sewer."""
        save_message = "Save absolute zetting put"
        output = save_shape(self, save_message)
        output_name = "{}.shp".format(output)
        # Create new layer abs_zetting_put of self.layer_rioolputten_joined
        self.layer_abs_zetting_put = QgsVectorFileWriter.writeAsVectorFormat(
            self.layer_rioolputten_joined, output_name,
            "CP1250", None, "ESRI Shapefile")
        # Add the layer to the map
        self.layer_abs_zetting_put = add_layer(self.iface, output_name)
        # Add field (abs_zet)
        self.layer_abs_zetting_put.dataProvider().addAttributes(
            [QgsField("abs_zet", QVariant.Double)])
        self.layer_abs_zetting_put.updateFields()

        # # # Create polygon of raster (dem)
        # # # https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#polygonize-a-raster-band
        # # # Polygonize of QGIS python
        # # # Point sampling(?) --> toolbox QGIS
        # # # Zonal statistics
        # # # http://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
        # from osgeo import gdal, ogr
        # import sys
        # # this allows GDAL to throw Python Exceptions
        # gdal.UseExceptions()
        # #
        # #  get raster datasource
        # #
        # src_ds = gdal.Open( "INPUT.tif" )
        # if src_ds is None:
        #     print 'Unable to open %s' % src_filename
        #     sys.exit(1)
        # try:
        #     srcband = src_ds.GetRasterBand(3)
        # except RuntimeError, e:
        #     # for example, try GetRasterBand(10)
        #     print 'Band ( %i ) not found' % band_num
        #     print e
        #     sys.exit(1)
        # #
        # #  create output datasource
        # #
        # dst_layername = "POLYGONIZED_STUFF"
        # drv = ogr.GetDriverByName("ESRI Shapefile")
        # dst_ds = drv.CreateDataSource( dst_layername + ".shp" )
        # dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )
        # gdal.Polygonize( srcband, None, dst_layer, -1, [], callback=None )

        # Calculate field
        import datetime
        current_year = datetime.datetime.now().year
        # abolute zetting = putten_stats_avg_pnt_li * (current_year - Jaar)
        self.layer_abs_zetting_put.startEditing()
        for feature in self.layer_abs_zetting_put.getFeatures():
            if isinstance(feature["avg_pnt_li"], float):
                if isinstance(feature["Jaar"], unicode):
                    abs_zet = feature["avg_pnt_li"] * float(current_year - int(
                        feature["Jaar"]))
                    feature["abs_zet"] = abs_zet
                    self.layer_abs_zetting_put.updateFeature(feature)
        self.layer_abs_zetting_put.commitChanges()

    def gem_abs_zet_rioolgebied(self):
        """Bepaal de gemiddelde absolute zetting van een rioolgebied."""
        # Referentie naar de absolute zetting per put -->
        # self.layer_abs_zetting_put
        # Aggregeer absolute zetting naar de gebiedsgrenzen
        save_message = "Save gemiddelde absolute zetting rioolgebied"
        self.layer_gem_abs_zetting_rioolgebied = self.aggregeer_putten(
            self.layer_gebiedsgrenzen, self.layer_abs_zetting_put, save_message
        )
        # Rename field to mean absolute zetting rioolgebied
        # # Spatial index maakt dit sneller!

    def gem_jaar_aanleg_rioolgebied(self):
        """Bepaal de gemiddelde absolute zetting van een rioolgebied."""
        # Referentie naar de absolute zetting per put -->
        # self.layer_abs_zetting_put
        # Rename field to mean jaar aanleg rioolgebied
        # # Spatial index maakt dit sneller!

        # Aggregeer absolute zetting naar de gebiedsgrenzen
        save_message = "Save gemiddelde jaar aanleg rioolgebied"
        self.layer_gem_jaar_aanleg_rioolgebied = self.aggregeer_putten(
            self.layer_gebiedsgrenzen, self.layer_abs_zetting_put, save_message
        )
        # Add label to layer
        field = self.dockwidget.r_i_kolom_jaar_van_aanleg_text.text()
        self.layer_gem_jaar_aanleg_rioolgebied = add_label_to_layer(
            self.iface, self.layer_gem_jaar_aanleg_rioolgebied, field)

    def jaar_van_falen_rioolgebied(self):
        """Function to calculate the year of failure of the sewer area."""
        save_message = "Save jaar van falen rioolgebied"
        output = save_shape(self, save_message)
        output_name = "{}.shp".format(output)
        # Create new layer jaar_van_falen of self.layer_rioolputten_joined
        self.layer_jaar_van_falen = QgsVectorFileWriter.writeAsVectorFormat(
            self.layer_gem_abs_zetting_rioolgebied, output_name,
            "CP1250", None, "ESRI Shapefile")
        # Add the layer to the map
        self.layer_jaar_van_falen = add_layer(self.iface, output_name)
        # Add field (jaar_van_falen_field)
        jaar_van_falen_field = "jaar_falen"
        self.layer_jaar_van_falen.dataProvider().addAttributes(
            [QgsField(jaar_van_falen_field, QVariant.Double)])
        self.layer_jaar_van_falen.updateFields()
        # Calculate field
        jaar_van_aanleg_field = self.dockwidget.r_i_kolom_jaar_van_aanleg_text.text()
        max_restzettingseis = float(
            self.dockwidget.r_i_max_restzettingseis_text.text()) / 100
        # Jaar van falen =
        # jaar_van_aanleg_field + abs(max_restzettingseis / "avg_pnt__1")
        self.layer_jaar_van_falen.startEditing()
        for feature in self.layer_jaar_van_falen.getFeatures():
            jaar_van_falen_value = int(round(float(
                feature[jaar_van_aanleg_field]) + abs(
                max_restzettingseis / float(feature["avg_pnt_li"]))))
            feature[jaar_van_falen_field] = jaar_van_falen_value
            self.layer_jaar_van_falen.updateFeature(feature)
        self.layer_jaar_van_falen.commitChanges()
        # Add label to layer
        self.layer_jaar_van_falen = add_label_to_layer(
            self.iface, self.layer_jaar_van_falen, jaar_van_falen_field)

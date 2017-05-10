# # -*- coding: utf-8 -*-
# """Module for creating a layer."""
import re

from PyQt4.QtCore import QVariant
from qgis.core import QgsField
from qgis.core import QgsGeometry
from qgis.core import QgsPalLayerSettings
from qgis.core import QgsPoint


# def create_memorylayer_of_shapefilelayer(shapefile_layer, layer_name):
#     """Function to create a memory layer of a shapefile layer."""
#     # Create the layer
#     geometry_type = "Point"
#     memory_layer = QgsVectorLayer("{}?crs={}".format(geometry_type, EPSG3857),
#                                   layer_name, "memory")
#     # Add the layer
#     QgsMapLayerRegistry.instance().addMapLayer(memory_layer)
#     # Add the attributes to the layer
#     add_attributes(memory_layer, shapefile_layer)
#     # Add the features to the shapefile_layer
#     add_features(memory_layer, shapefile_layer)
#     # Return the layer
#     return memory_layer


def add_layer(iface, file):
    """Function to create a vector layer of a shapefile."""
    layer_name = re.sub(r".*/", "", file)
    layer_name = re.sub(r".shp", "", layer_name)
    layer = iface.addVectorLayer(
        file,
        layer_name,
        "ogr")
    # Return the layer
    return layer


def add_attribute(layer, name, type):
    """Add a field to a vector layer."""
    if type == "integer":
        layer.dataProvider().addAttributes([QgsField(name, QVariant.Int)])
    elif type == "float":
        layer.dataProvider().addAttributes([QgsField(name, QVariant.Double)])
    elif type == "string":
        layer.dataProvider().addAttributes([QgsField(name, QVariant.String)])
    layer.updateFields()


def add_attributes(memory_layer, shapefile_layer):
    """Function to add attributes from a shapefile layer to a memory layer."""
    # Create the attributes
    fields = [field for field in shapefile_layer.pendingFields()]
    # Add the attributes to the layer
    memory_layer.dataProvider().addAttributes(fields)
    memory_layer.updateFields()


def add_features(memory_layer, shapefile_layer):
    """Function to add features to the layer."""
    # Create the features
    memory_layer.startEditing()
    features = []
    for feature in shapefile_layer.getFeatures():
        new_feature = feature
        new_feature.setGeometry(
            QgsGeometry.fromPoint(QgsPoint(feature["X"], feature["Y"])))
        features.append(new_feature)
    # add the features
    memory_layer.dataProvider().addFeatures(features)
    memory_layer.commitChanges()


# def join_layers_by_attribute(target_layer, target_field, input_layer,
#                              input_field):
#     """
#     Function to add attributes from a shapefile layer to a memory layer."""
#     # Add missing fields
#     add_attributes(target_layer, input_layer)
#     join_object = QgsVectorJoinInfo()
#     join_object.joinLayerId = input_layer.id()
#     join_object.joinFieldName = input_field
#     join_object.targetFieldName = target_field
#     target_layer.addJoin(join_object)  # You should get True as response
#     # add input_field ass attribute


# def show_shape(self, file):
#     """Function to show a shapefile in the Table of Contents."""
#     output_name = "{}.shp".format(file)  # output = file
#     # Add the layer to the map
#     layer_name = re.sub(r"[a-zA-Z_0-9]*/", "", output_name)
#     layer_name = re.sub(r"[a-zA-Z_0-9]*.", "", layer_name)
#     layer_name = re.sub(r".*[a-zA-Z_0-9]", "", layer_name)
#     layer = self.iface.addVectorLayer(output_name, layer_name, "ogr")
#     return layer

def add_label_to_layer(iface, layer, field):
    """Function to add a label to a layer."""
    # Add label.layer.setCustomProperty("labeling", "Jaar")
    layer.setCustomProperty("labeling/enabled", "true")
    layer.setCustomProperty("labeling/fontFamily", "Arial")
    layer.setCustomProperty("labeling/fontSize", "10")
    layer.setCustomProperty("labeling/fieldName", field)
    layer.setCustomProperty("labeling/placement", "2")
    label = QgsPalLayerSettings()
    label.readFromLayer(layer)
    label.enabled = True
    label.fieldName = field
    label.writeToLayer(layer)
    layer.setCustomProperty("labeling/drawLabels", "True")
    iface.mapCanvas().refresh()
    # Return the layer
    return layer

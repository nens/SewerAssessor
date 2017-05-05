# # -*- coding: utf-8 -*-
# """Module for creating a layer."""
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer
from qgis.core import QgsGeometry
from qgis.core import QgsPoint
# from qgis.core import QgsExpression
# from qgis.core import QgsFeatureRequest
from qgis.core import QgsVectorJoinInfo

from .constants import EPSG3857


def create_memorylayer_of_shapefilelayer(shapefile_layer, layer_name):
    """Function to create a memory layer of a shapefile layer."""
    # Create the layer
    geometry_type = "Point"
    memory_layer = QgsVectorLayer("{}?crs={}".format(geometry_type, EPSG3857),
                                  layer_name, "memory")

    # Add the layer
    QgsMapLayerRegistry.instance().addMapLayer(memory_layer)

    # Add the attributes to the layer
    add_attributes(memory_layer, shapefile_layer)

    # Add the features to the layer
    add_features(memory_layer, shapefile_layer)

    # Return the layer
    return memory_layer


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


def join_layers_by_attribute(target_layer, target_field, input_layer,
                             input_field):
    """Function to add attributes from a shapefile layer to a memory layer."""
    # Add missing fields
    add_attributes(target_layer, input_layer)
    join_object = QgsVectorJoinInfo()
    join_object.joinLayerId = input_layer.id()
    join_object.joinFieldName = input_field
    join_object.targetFieldName = target_field
    target_layer.addJoin(join_object)  # You should get True as response
    # add input_field ass attribute

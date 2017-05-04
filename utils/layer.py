# # -*- coding: utf-8 -*-
# """Module for creating a layer."""
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer
from qgis.core import QgsGeometry
from qgis.core import QgsPoint
from qgis.core import QgsExpression
from qgis.core import QgsFeatureRequest

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


def join_layers(memory_layer, shapefile_layer):
    """Function to add attributes from a shapefile layer to a memory layer."""
    # Add missing fields
    add_attributes(memory_layer, shapefile_layer)
    # Fill empty fields
    for feature_memory in memory_layer.getFeatures():
            try:
                exp = QgsExpression(
                    u'putcode ILIKE {}{}{}'.format(
                        "'%", feature_memory["Knoopnr"], "%'"))
                request = QgsFeatureRequest(exp)
                requested_features = shapefile_layer.getFeatures(request)
                for requested_feature in requested_features:
                    feature_memory.setAttribute(
                        "vir_pnt_id", requested_feature["vir_pnt_id"])
                    feature_memory.setAttribute(
                        "putcode", requested_feature["putcode"])
                    feature_memory.setAttribute(
                        "object_gui", requested_feature["object_gui"])
                    feature_memory.setAttribute(
                        "buffer_siz", requested_feature["buffer_siz"])
                    feature_memory.setAttribute(
                        "num_points", requested_feature["num_points"])
                    feature_memory.setAttribute(
                        "w_pnt_line", requested_feature["w_pnt_line"])
                    feature_memory.setAttribute(
                        "avg_pnt_li", requested_feature["avg_pnt_li"])
                    feature_memory.setAttribute(
                        "stddev_pnt", requested_feature["stddev_pnt"])
                    feature_memory.setAttribute(
                        "min_pnt_li", requested_feature["min_pnt_li"])
                    feature_memory.setAttribute(
                        "max_pnt_li", requested_feature["max_pnt_li"])
                    feature_memory.setAttribute(
                        "max_diff_p", requested_feature["max_diff_p"])
                    feature_memory.setAttribute(
                        "ogc_fid", requested_feature["ogc_fid"])
                    memory_layer.updateFields()
                    print 'new feature added{}'.format(
                        requested_feature["putcode"])
                    break
            except:
                print 'no feature'

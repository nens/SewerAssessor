# Changelog

## 0.1 (unreleased)

### Features
- Add a change log
- Add a readme
* Mock-up dockwidget for assessing sewer properties
#### 'Restlevensduur' tab
##### Input
* Browse files for "Restlevensduur" tab
##### Output
###### 'Gem. zettingssnelheid put'
* Shows input as vector layer ('Gem. zettingssnelheid put' and 'Riool putten')
* Creates shapefile of output (join of input layers)
* Shows output as vector layer on the map
###### 'Gem. zettingssnelheid rioolgebied'
* Shows 'Gebiedsgrenzen' as vector layer
* Creates shapefile of output (aggregation of 'Gem zettingssnelheid put' to the boundaries of 'Gebiedsgrenzen')
* Shows output as vector layer on the map
###### 'St.dev zetting rioolgebied'
###### Absolute zetting put
* Creates shapefile of output (output of 'Gem. zettingssnelheid rioolgebied' with added, calculated, field 'abs_zet')
* Shows output as vector layer on the map
###### 'Gem. abs. zetting rioolgebied'
* Creates shapefile of output (aggregation of output of 'Absolute zetting put' to the boundaries of 'Gebiedsgrenzen')
* Shows output as vector layer on the map
###### 'Gem. jaar van aanleg rioolgebied'
* Creates shapefile of output (aggregation of output of 'Absolute zetting put' to the boundaries of 'Gebiedsgrenzen')
* Shows output as vector layer on the map, labelled with field 'Jaar'
###### 'Jaar van falen rioolgebied'
* Creates shapefile of output (output of 'Gem. abs zetting rioolgebied' to the boundaries of 'Gebiedsgrenzen' with added, calculated field 'jaar_falen')
* Shows output as vector layer on the map, labelled with field 'jaar_falen'
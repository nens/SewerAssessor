# SewerAssessor
QGIS plug-in for assessing properties of the sewer.

## Features
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

## Requirements
* QGIS 2.14

## Installation
The plug-in can be added using one of the following ways:
* Use the Lizard QGIS repository
  * via the QGIS menu bar go to Plugins > Manage And Install Plugins... > Settings
  * add `https://plugins.lizard.net/plugins.xml` and reload
  * install the plugin by selecting SewerAssessor
* Copy or symlink the repo directory to your plugin directory
  * on *Linux*: `~/.qgis2/python/plugins`
  * on *Windows*: `C:\\Users\<username>\.qgis2\python\plugins\`
  * make sure the dir is called `SewerAssessor`. 

## Release
Make sure you have `zest.releaser` with `qgispluginreleaser` installed. To make a release (also see: [1]):
```
$ cd /path/to/the/plugin`
$ fullrelease  # NOTE: if it asks you if you want to check out the tag press 'y'.
```

Manually copy to server:
```
$ scp SewerAssessor.0.1.zip <user.name>@packages-server.example.local:/srv/packages.lizardsystem.nl/var/plugins
```

## Tests
There are currently 4 tests (in the test folder).
These tests can be run by using `make test` [2].

## Other interesting QGIS plug-ins:
* [3Di QGIS plug-in](https://github.com/nens/threedi-qgis-plugin)
* [LizardViewer](https://github.com/nens/LizardViewer)

## Notes
[1]: Under the hood it calls `make zip` (see `Makefile`, the old zip directive is overwritten).
[2]: Make test uses `nose`. Make sure you have `nose` installed (`pip install nose`). And make sure the plugin dir has the right package name, is `SewerAssessor` or else the relative imports won't work correctly. Then run `nosetests` inside the plugin directory:
```
$ nosetests --with-doctest
```
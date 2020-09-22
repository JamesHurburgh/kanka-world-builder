"""
Parses a *.map file from Azgaar's Fantasy-Map-Generator into a *.json String.

For the map generator see:

https://github.com/Azgaar/Fantasy-Map-Generator/

Most of the code in here is copied/translated from 

https://github.com/Azgaar/Fantasy-Map-Generator/blob/master/modules/save-and-load.js

Doesn't copy all generated data, only:

    -mapVersion
    -archive
    -biomesData,
    -mapCoordinates,
    -notes,
    -seed,
    -biomes,
    -grid,
    -pack,    
    
Usage example:

    python3 -i fmg_map_to_json.py ~/home/user/mapfile.map
    
"""
# & C:/Python38/python.exe .\convert-map.py '.\Foyersia 2020-09-23-00-39.map'
import sys
import os
import json
import re
import math
import itertools

path = sys.argv[1]

assert path.endswith(".map")

byte_string = b''

file = open(path, "rb")

for line in file:
    byte_string += line
  
version = '1.4' #hardcoded. This code is only guaranteed to work for this version.
    
data = byte_string.split(b"\r\n")
mapVersion = data[0].split(b'|')[0].decode() or data[0].decode()
print("Loading Fantasy-Map-Generator Mapfile-Version {}".format(mapVersion))
archive = "<a href='https://github.com/Azgaar/Fantasy-Map-Generator/wiki/Changelog' target='_blank'>archived version</a>"

parsed = float(re.sub("[a-z]*", "", mapVersion.lower())) #Not quite the same as js parseFloat, But should suffice for conventional versioning.

message = ""
load = False

print(f'{len(data)} data packs loaded')
if math.isnan(parsed) or len(data) < 26 or not data[5]:
    message = 'The file you are trying to load is outdated or not a valid .map file. <br>Please try to open it using an {archive}'
    print("Alert! " + message)
    print ("Version conflict!")
elif(parsed < 0.7):
    message = 'The map version you are trying to load ({mapVersion}) is too old and cannot be updated to the current version.<br>Please keep using an {archive}'
    print("Alert! " + message)
    print ("Version conflict!")
else:
  load = True
  #message =  'The map version ({}) does not match the Generator version ({}). The map will be auto-updated. <br>In case of issues please keep using an {} of the Generator'.format(mapVersion, version, archive)



"""
Initialize biomesData as in 'applyDefaultBiomesSystem()' in 'main.js'
"""
biomesData = {}
biomesData["name"] = ["Marine","Hot desert","Cold desert","Savanna","Grassland","Tropical seasonal forest","Temperate deciduous forest","Tropical rain forest","Temperate rain forest","Taiga","Tundra","Glacier"]
biomesData["color"] = ["#53679f","#fbe79f","#b5b887","#d2d082","#c8d68f","#b6d95d","#29bc56","#7dcb35","#45b348","#4b6b32","#96784b","#d5e7eb"]

biomesData["i"] = list(range(0, len(biomesData["name"])))
#biomesData["habitability"] = [0,2,5,15,25,50,100,80,90,10,2,0]
#iconsDensity = [0,3,2,120,120,120,120,150,150,100,5,0]
#//const icons = [{},{dune:1},{dune:1},{acacia:1, grass:9},{grass:1},{acacia:1, palm:1},{deciduous:1},{acacia:7, palm:2, deciduous:1},{deciduous:7, swamp:3},{conifer:1},{grass:1},{}]
#const icons = [{},{dune:3, cactus:6, deadTree:1},{dune:9, deadTree:1},{acacia:1, grass:9},{grass:1},{acacia:8, palm:1},{deciduous:1},{acacia:5, palm:3, deciduous:1, swamp:2},{deciduous:5, swamp:3},{conifer:1},{grass:1},{}]
#const cost = new Uint8Array([10,200,150,60,50,70,70,80,90,80,100,255]) // biome movement cost
biomesData["biomesMartix"] = [
  [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
  [3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,9,9,9,9,9,10,10],
  [5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,9,9,9,9,9,10,10,10],
  [5,6,6,6,6,6,6,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,10,10,10],
  [7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,10,10,10]
  ]

# Parse params
params = data[0].split(b"|")

if params[3]:
    seed = params[3].decode()
"""
if (params[4]):
    graphWidth = +params[4] #Not implemented
if (params[5]):
    graphHeight = +params[5] #Not implemented
"""

# Parse settings
settings_mapping = [
    "distanceUnitInput",
    "distanceScaleInput",
    "areaUnit",
    "heightUnit",
    "heightExponentInput",
    "temperatureScale",
    "barSize",
    "barLabel",
    "barBackOpacity",
    "barBackColor",
    "barPosX",
    "barPosY",
    "populationRate",
    "urbanization",
    "mapSizeOutput",
    "latitudeOutput",
    "temperatureEquatorOutput",
    "temperaturePoleOutput",
    "precOutput",
    "stringify_options",
    "mapName"
]
settings = {}
settings_data = [b.decode() for b in data[1].split(b"|")]

for i, setting in enumerate(settings_data):
    if setting and settings_mapping[i]:
        settings[settings_mapping[i]] = str(setting)

settings["stringify_options"] = None

""" Parse config """
if (data[2]):
    mapCoordinates = json.loads(data[2])
if (data[4]):
    notes = json.loads(data[4])
    
""" Parse biomes """
biomes = [b.decode() for b in data[3].split(b"|")]

""" Parse name """
name = biomes[2].split(",")

if (len(name) != len(biomesData["name"])):
    print("Biomes data is not correct and will not be loaded")

biomesData["color"] = biomes[0].split(",")
#biomesData.habitability = biomes[1].split(",").map(h => +h)
biomesData["name"] = name

# Parse grid data
# Keep the actual data as string (no UintArray)
grid = json.loads(data[6])
grid["cells"] = {}
#calculateVoronoi(grid, grid.points) #Not implemented
grid["cells"]["h"] = [b.decode() for b in (data[7].split(b","))]
grid["cells"]["prec"] = [b.decode() for b in (data[8].split(b","))]
grid["cells"]["f"] = [b.decode() for b in (data[9].split(b","))]
grid["cells"]["t"] = [b.decode() for b in (data[10].split(b","))]
grid["cells"]["temp"] = [b.decode() for b in (data[11].split(b","))]

"""
Parse Pack data
"""
pack = {}
#reGraph() #Not implemented
#reMarkFeatures() #Not implemented
pack["features"] = json.loads(data[12])
pack["cultures"] = json.loads(data[13])
pack["states"] = json.loads(data[14])
pack["burgs"] = json.loads(data[15])
pack["religions"] = json.loads(data[29])
pack["provinces"] = json.loads(data[30])
# pack["namesData"] = json.loads(data[31])
pack["rivers"] = json.loads(data[32])

pack["cells"] = {}

pack["cells"]["biome"] = [b.decode() for b in(data[16].split(b","))]
pack["cells"]["burg"] = [b.decode() for b in(data[17].split(b","))]
pack["cells"]["conf"] = [b.decode() for b in(data[18].split(b","))]
pack["cells"]["culture"] = [b.decode() for b in(data[19].split(b","))]
pack["cells"]["fl"] = [b.decode() for b in(data[20].split(b","))]
pack["cells"]["pop"] = [b.decode() for b in(data[21].split(b","))]
pack["cells"]["r"] = [b.decode() for b in(data[22].split(b","))]
pack["cells"]["road"] = [b.decode() for b in(data[23].split(b","))]
pack["cells"]["s"] = [b.decode() for b in(data[24].split(b","))]
pack["cells"]["state"] = [b.decode() for b in(data[25].split(b","))]
pack["cells"]["religions"] = [b.decode() for b in(data[26].split(b","))]
pack["cells"]["provinces"] = [b.decode() for b in(data[27].split(b","))]

"""
Output data as .json to current directory.
"""
parsed_data = {
    "mapVersion" : mapVersion,
    "settings" : settings,
    "archive" : archive,
    "biomesData" : biomesData,
    "mapCoordinates" : mapCoordinates,
    "notes" : notes,
    "seed" : seed,
    "biomes" : biomes,
    "grid" : grid,
    "pack" : pack,    
    }

"""
Save parsed_data at *.map location as json.
"""

out_path = os.path.splitext(path)[0] + ".json"
print("Writing file to: " + out_path)
with open(out_path, "w") as outfile:
    json.dump(parsed_data, outfile, indent=4)
    print("Successfully saved data to {}".format(out_path))
    outfile.close()

# SVG file
out_path = os.path.splitext(path)[0] + ".svg"
print("Writing file to: " + out_path)
with open(out_path, "wb") as outfile:
    outfile.write(data[5])
    outfile.close()
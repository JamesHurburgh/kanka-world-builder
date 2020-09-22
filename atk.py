__author__ = "James Hurburgh"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "James Hurburgh"
__email__ = "JamesHurburgh@gmail.com"
__status__ = "Prototype"

# Usage:
#  Windows:
#   & C:/Python38/python.exe .\atk.py '.\Foyersia 2020-09-08-00-00.json'

import json
import sys

from config import options

import e_world
import e_timelines
import e_rivers
import e_biomes
import e_states
import e_provinces
import e_burgs

path = sys.argv[1]
assert path.endswith(".json")

with open(path,'rb') as mapfile:
    mapstring = mapfile.read()
    map = json.loads(mapstring)

worldData = {}
worldData["map"] = map

e_world.Parse(worldData)
e_biomes.Parse(worldData)
e_timelines.Parse(worldData)
e_rivers.Parse(worldData)
e_states.Parse(worldData)
e_provinces.Parse(worldData)
e_burgs.Parse(worldData)

from config import options
import kankaapi

def Parse(worldData=None):
    if not options["entities.biomes"]:
        return
    if worldData == None:
        print('No world data.')
    if worldData["map"] == None:
        print('No map loaded.')

    print(f'Parsing Biomes')
    worldData["biome_data"] = {}
    biomes = worldData["map"]["biomesData"]
    for biomeId in biomes["i"]:
        print(f' Parsing {biomes["name"][biomeId]}')
        note = {
            "name" : biomes["name"][biomeId],
            "entry": "\n<p>Lorem Ipsum.</p>\n",
            "is_private": False,
            "type": "Biome"
        }
        response = kankaapi.create('notes', note)
        worldData["biome_data"][biomeId] = {
            "note_id" : response["data"]["id"],
            "entity_id" : response["data"]["entity_id"],
        }
from config import options
import kankaapi

def Parse(worldData=None):
    if not options["entities.world"]:
        return
    if worldData == None:
        print('No world data.')
    if worldData["map"] == None:
        print('No map loaded.')

    print(f'Parsing {worldData["map"]["settings"]["mapName"]} (World)')
    location = { 
        "name" : worldData["map"]["settings"]["mapName"],
        "image_url" : None,
        "entry": "\n<p>Lorem Ipsum.</p>\n",
        "is_private": False,
        "type": "World"
    }
    response = kankaapi.create('locations', location)

    worldData["world_location_id"] = response["data"]["id"]
    worldData["world_entity_id"] = response["data"]["entity_id"]
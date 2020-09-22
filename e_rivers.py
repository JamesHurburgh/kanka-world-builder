from config import options
import kankaapi

def Parse(worldData=None):
    if not options["entities.rivers"]:
        return
    if worldData == None:
        print('No world data.')
    if worldData["map"] == None:
        print('No map loaded.')

    print(f'Parsing Rivers')
    worldData["riverIds"] = {}
    rivers = worldData["map"]["pack"]["rivers"]
    for river in rivers:
        print(f' Parsing {river["name"]} {river["type"]}')
        location = {
            "name" : f'{river["name"]} {river["type"]}',
            "entry": "\n<p>Lorem Ipsum.</p>\n",
            "parent_location_id" : worldData["world_location_id"],
            "is_private": False,
            "type": "Watercourse"
        }
        response = kankaapi.create('locations', location)
        worldData["riverIds"][river["i"]] = {
            "location_id" : response["data"]["id"],
            "entity_id" : response["data"]["entity_id"],
        }

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

    # RIVERS Parents and other attributes
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
        "entry": GenerateEntry(worldData),
        "is_private": False,
        "type": "World"
    }
    response = kankaapi.create('locations', location)

    worldData["world_location_id"] = response["data"]["id"]
    worldData["world_entity_id"] = response["data"]["entity_id"]

def GenerateEntry(world):
    # count biomes
    biomeCount = {}
    total = 0
    
    for biome in world["map"]["pack"]["cells"]["biome"]:
        biomeCount[biome] = biomeCount.get(biome, 0) + 1
        total += 1

    sortedBiomeCount = sorted(biomeCount.items(), key=lambda x: x[1], reverse=True)
    biomesString = f'<h2>Biomes</h2>'

    for biomeTuple in sortedBiomeCount:
        biomeId = biomeTuple[0]
        count = biomeTuple[1]
        percent = count / total * 100
        biomesString += f'<p>{world["map"]["biomesData"]["name"][int(biomeId)]} : {format(percent, ".2f")}%</p>'
    print(total)

    return f"\n{biomesString}\n"
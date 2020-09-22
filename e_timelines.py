from config import options
import kankaapi

def Parse(worldData=None):
    if not options["entities.timelines"]:
        return
    if worldData == None:
        print('No world data.')
    if worldData["map"] == None:
        print('No map loaded.')
    
    mapName = worldData["map"]["settings"]["mapName"]

    # Timeline
    print(f'Parsing {mapName} Timeline')
    timeline = {
        "name" : f'{mapName} Timeline',
        "type": "Global",
        "is_private": False
    }
    response = kankaapi.create('timelines', timeline)
    worldData["world_timeline_id"] = response["data"]["id"]
    worldData["world_timeline_entity_id"] = response["data"]["entity_id"]

    # Era
    print(f'Parsing {mapName} Current Era')
    era = {
        "timeline_id": worldData["world_timeline_id"],
        "name": "Current",
        "abbreviation": "C",
        "start_year": 0,
        "end_year": None,
        "visiblity": "all"
    }
    response = kankaapi.create(f'timelines/{worldData["world_timeline_id"]}/timeline_eras', era)
    worldData["era_id"] = response["data"]["id"]
from config import options
import kankaapi
import ironarachne

def Parse(worldData=None):
    if not options["entities.provinces"]:
        return
    if worldData == None:
        print('No world data.')
    if worldData["map"] == None:
        print('No map loaded.')

    print(f'Parsing Provinces:')
    worldData["provinceIds"] = {}
    stateIds = worldData["stateIds"]
    provinces = worldData["map"]["pack"]["provinces"][1:]
    seed = worldData["map"]["seed"]

    for province in provinces:
        if province["state"] in stateIds:
            print(f' Parsing {province["fullName"]} (Province)')
            if options["heraldry"]:
                image_url = ironarachne.getHeraldryLink(seed, f'p{province["i"]}')
            else:
                image_url = None

            location = { 
                "name" : province["fullName"],
                "image_url" : image_url,
                "entry": "\n<p>Lorem Ipsum.</p>\n",
                "parent_location_id" : stateIds[province["state"]]["location_id"],
                "is_private": False,
                "type": "Province"
            }
            response = kankaapi.create('locations', location)
            entity_id = response["data"]["entity_id"]
            # Save the created ids for later
            worldData["provinceIds"][province["i"]] = {
                "location_id" : response["data"]["id"],
                "entity_id" : entity_id,
            }
            # Attributes
            if options["attributes"]:
                print(f'  : creating attributes')
                kankaapi.createAttribute("Name", str(province["name"]), entity_id=entity_id)
                kankaapi.createAttribute("Form Name", str(province["formName"]), entity_id=entity_id)

from config import options
import kankaapi
import ironarachne

def Parse(worldData=None):
    if not options["entities.burgs"]:
        return
    if worldData == None:
        print('No world data.')
    if worldData["map"] == None:
        print('No map loaded.')

    print(f'Parsing Burgs:')
    # features = ["capital", "port", "citadel", "plaza", "walls", "shanty", "temple"]
    worldData["burgIds"] = {}
    map = worldData["map"]
    burgs = map["pack"]["burgs"][1:]
    seed = map["seed"]
    gridCells = map["grid"]["cells"]
    cells = map["pack"]["cells"]
    biomes = map["biomesData"]
    rivers = map["pack"]["rivers"]
    cultures = map["pack"]["cultures"]
    religions = map["pack"]["religions"]

    for burg in burgs[1:100]:
        if burg["state"] in worldData["stateIds"]:
            print(f' Parsing {burg["name"]} (Burg)')
            if options["heraldry"]:
                image_url = ironarachne.getHeraldryLink(seed, f'b{burg["i"]}')
            else:
                image_url = None

            cellId = burg["cell"]
            
            h = int(gridCells["h"][cellId])
            prec = int(gridCells["prec"][cellId])
            f = int(gridCells["f"][cellId])
            t = int(gridCells["t"][cellId])
            temp = int(gridCells["temp"][cellId])

            conf = int(cells["conf"][cellId])
            fl = int(cells["fl"][cellId])
            population = cells["pop"][cellId]
            riverId = int(cells["r"][cellId])

            biomeId = int(cells["biome"][cellId])
            provinceId = int(cells["provinces"][cellId])
            cultureId = int(cells["culture"][cellId])
            roadId = int(cells["road"][cellId])
            religionId = int(cells["religions"][cellId])

            biomeName = biomes["name"][biomeId]

            # print(f' cultureId {cultureId}')
            # print(f'   riverId {riverId}')
            # print(f'religionId {religionId}')
            culture = list(filter(lambda c: c["i"] == cultureId, cultures))[0]
            # road = list(filter(lambda r: r["i"] == roadId, roads))[0]
            if riverId != 0:
                river = list(filter(lambda r: r["i"] == riverId, rivers))[0]
            religion = list(filter(lambda r: r["i"] == religionId, religions))[0]
            
            print(f'h {h}')
            print(f'prec {prec}')
            print(f'f {f}')
            print(f't {t}')
            print(f'temp {temp}')
            print(f'provinceId {provinceId}')
            print(f'conf {conf}')
            print(f'fl {fl}')
            print(f'      road {roadId}')
            
            print(f'population {population}')
            print(f'     biome {biomeName}')
            print(f'   culture {culture}')
            print(f'     river {river}')
            print(f'  religion {religion}')

            location = { 
                "name" : burg["name"],
                "image_url" : image_url,
                "entry": "\n<p>Lorem Ipsum.</p>\n",
                "parent_location_id" : worldData["provinceIds"][provinceId]["location_id"],
                "is_private": False,
                "type": "Burg"
            }
            response = kankaapi.create('locations', location)
            # Save the created ids for later
            worldData["burgIds"][burg["i"]] = {
                "location_id" : response["data"]["id"],
                "entity_id" : response["data"]["entity_id"],
            }

            entity_id = response["data"]["entity_id"]
            # Attributes
            if options["attributes"]:
                print(f'  Parsing attributes')
                kankaapi.createAttribute("Name", str(burg["name"]), entity_id=entity_id)
                kankaapi.createAttribute("Population", str(round(burg["population"] * 1000)), entity_id=entity_id)
                kankaapi.createAttribute("Is Capital", str(burg["capital"] == 1), entity_id=entity_id, att_type="checkbox")
                kankaapi.createAttribute("Has port", str(burg["port"] == 1), entity_id=entity_id, att_type="checkbox")
                kankaapi.createAttribute("Has citadel", str(burg["citadel"] == 1), entity_id=entity_id, att_type="checkbox")
                kankaapi.createAttribute("Has plaza", str(burg["plaza"] == 1), entity_id=entity_id, att_type="checkbox")
                kankaapi.createAttribute("Has walls", str(burg["walls"] == 1), entity_id=entity_id, att_type="checkbox")
                kankaapi.createAttribute("Has shanty town", str(burg["shanty"] == 1), entity_id=entity_id, att_type="checkbox")
                kankaapi.createAttribute("Has temple", str(burg["temple"] == 1), entity_id=entity_id, att_type="checkbox")

            
        
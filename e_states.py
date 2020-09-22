from config import options
import kankaapi
import ironarachne

def Parse(worldData=None):
    if not options["entities.states"]:
        return
    if worldData == None:
        print('No world data.')
    if worldData["map"] == None:
        print('No map loaded.')

    diplomacyValues = {
        "Ally" : { "attitude" : 50, "colour" : "#00b300"},
        "Friendly" : { "attitude" : 25, "colour" : "#d4f8aa"},
        "Neutral" : { "attitude" : 0, "colour" : "#edeee8"},
        "Suspicion" : { "attitude" : -25, "colour" : "#eeafaa"},
        "Enemy" : { "attitude" : -100, "colour" : "#e64b40"},
        "Unknown" : { "attitude" : 0, "colour" : "#a9a9a9"},
        "Rival" : { "attitude" : -50, "colour" : "#ad5a1f"},
        "Vassal" : { "attitude" : 100, "colour" : "#87CEFA"},
        "Suzerain" : { "attitude" : 100, "colour" : "#00008B"},
    }

    print(f'Parsing States')
    worldData["stateIds"] = {}
    states = worldData["map"]["pack"]["states"]
    seed = worldData["map"]["seed"]

    for state in states:
        if state["name"] != "Neutrals":
            print(f' Parsing {state["fullName"]} (State)')
            if options["heraldry"]:
                image_url = ironarachne.getHeraldryLink(seed, f's{state["i"]}')
            else:
                image_url = None

            location = { 
                "name" : state["fullName"],
                "image_url" : image_url,
                "entry": "\n<p>Lorem Ipsum.</p>\n",
                "parent_location_id" : worldData["world_location_id"],
                "is_private": False,
                "type": "State"
            }
            response = kankaapi.create('locations', location)
            entity_id = response["data"]["entity_id"]
            worldData["stateIds"][state["i"]] = {
                "location_id" : response["data"]["id"],
                "entity_id" : entity_id,
            }

            if options["attributes"]:
                print(f'  Parsing attributes')
                kankaapi.createAttribute("Name", str(state["name"]), entity_id=entity_id)
                kankaapi.createAttribute("Form", str(state["form"]), entity_id=entity_id)
                kankaapi.createAttribute("Form Name", str(state["formName"]), entity_id=entity_id)
                kankaapi.createAttribute("Burgs", str(state["burgs"]), entity_id=entity_id)
                kankaapi.createAttribute("Area", f'~{str(state["area"])} acres', entity_id=entity_id)
                kankaapi.createAttribute("Type", str(state["type"]), entity_id=entity_id)
                kankaapi.createAttribute("Expansionism", str(state["expansionism"]), entity_id=entity_id)
                kankaapi.createAttribute("Total Population", "{Urban Population}+{Rural Population}", entity_id=entity_id)
                kankaapi.createAttribute("Urban Population", str(round(state["urban"] * 1000)), entity_id=entity_id)
                kankaapi.createAttribute("Rural Population", str(round(state["rural"] * 1000)), entity_id=entity_id)
                kankaapi.createAttribute("Military Alert", str(state["alert"]), entity_id=entity_id)
            
            # TODO sort by date while adding
            if options["entities.states.history"]:
                print(f'  Parsing history')
                timelineId = worldData["world_timeline_id"]
                eraId = worldData["era_id"]
                for campaign in state["campaigns"]:
                    print(f'   Parsing {campaign["name"]} (Campaign)')
                    element = {
                        # TODO add an actual calendar entity
                        "name" : campaign["name"],
                        "timeline_id": timelineId,
                        "era_id": eraId,
                        "date" : f'{campaign["start"]}-{campaign["end"]}',
                        "entry": f'\n<p>[location:{entity_id}] campaign from {campaign["start"]}-{campaign["end"]}.</p>\n',
                        "is_private": False,
                        "visiblity" : "all"
                    }
                    response = kankaapi.create(f'timelines/{timelineId}/timeline_elements', element)
            
    # relations   
    for state in states:
        if state["name"] == "Neutrals":
            continue
        state_entity_id = worldData["stateIds"][state["i"]]["entity_id"]
        if options["entities.states.neighbors"]:
            print(f' Parsing {state["fullName"]} neighbors relations')
            for neighbour in state["neighbors"]:
                if neighbour in worldData["stateIds"]:
                    target_id = worldData["stateIds"][neighbour]["entity_id"]
                    kankaapi.createRelation(relation = "Neighbour", owner_id = state_entity_id, target_id = target_id)
        if options["entities.states.diplomacy"]:
            print(f' Parsing {state["fullName"]} diplomacy relations')
            for i, diplomacy in enumerate(state["diplomacy"]):
                if i != 0 and i != state["i"] and (options["entities.states.diplomacy.all"] or (diplomacyValues[diplomacy]["attitude"] != 0)):
                    target_id = worldData["stateIds"][i]["entity_id"]
                    kankaapi.createRelation(
                        relation = diplomacy, 
                        owner_id = state_entity_id, 
                        target_id = target_id,
                        attitude = diplomacyValues[diplomacy]["attitude"],
                        colour = diplomacyValues[diplomacy]["colour"])
    

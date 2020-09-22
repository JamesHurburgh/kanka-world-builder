import requests
import json
import time
from config import options
from config import kanka_api

with open(kanka_api['token.filepath'],'r') as tokenFile:
    tokenString = tokenFile.read()

token = 'Bearer ' + tokenString
prefix = kanka_api['prefix']
campaignId = kanka_api['campaignId']

headers = { 'Authorization': token, 'Content-type': 'application/json' , 'Accept': 'application/json' }

campaign_url = prefix + 'campaigns/' + campaignId + '/'

def apiGet(url=None):
    response = requests.get(url, headers=headers)
    print(url + ' ' + str(response.status_code))
    return response

def apiPost(url=None, data=None, files=None):
    if options["debug"]:
        print(f'     url: {url}')
        print(f'    data: {data}')
    if options["active"]: 
        time.sleep(2) #Stupid way of rate limiting
        response = requests.post(url, headers=headers, files=files, json=data)
        if response.status_code >= 400:
            print(f'response: {str(response.status_code)}')
            print(f' content: {str(response.content)}')
        return response.json()
    else:
        data["data"] = {}
        data["data"]["id"] = 0
        data["data"]["entity_id"] = 0        
    return data

def get(entityType=None, id=None):
    if id is None:
        return json.loads(apiGet(campaign_url + entityType + '?page=1&related=1').text)
    else:
        return json.loads(apiGet(campaign_url + entityType + '/' + id).text)
        
def create(entityType=None, entity=None, files=None):
    return apiPost(campaign_url + entityType, entity)
    
def createAttribute(name="name", value="value", att_type="text", is_private=False, entity_id=None):
    attribute = {
        "name": name,
        "value": value,
        "type": att_type,
        "entity_id" : entity_id,
        "is_private": is_private
    }
    return create(f'entities/{entity_id}/attributes', attribute)
    
def createRelation(relation="relation", owner_id=0, target_id=0, attitude=0, colour=None, is_star=True, is_private=False):
    relation = {
        "relation": relation,
        "owner_id": owner_id,
        "target_id": target_id,
        "attitude": attitude,
        "colour": colour,
        "is_star" : is_star,
        "is_private" : is_private,
        "visibility" : "all"
    }
    return create(f'entities/{owner_id}/relations', relation)
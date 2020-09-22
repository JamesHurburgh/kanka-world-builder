options = {
                            'debug' : True,
                           'active' : True, # Will hit the Kanka api and create entities instead of just parsing them.
                         'heraldry' : False, # Will get heraldry from ironarachne.com and include in entities where appropriate 
                       'attributes' : False, # Will parse attributes on entities, not just the entities themselves.
                   'entities.world' : True, # This should always be true, otherwise many other things will fail.
               'entities.timelines' : False, # Parse Timelines
                  'entities.biomes' : False, # Parse Biomes
                  'entities.rivers' : False, # Parse Rivers
                  'entities.states' : False, # Parse States
        'entities.states.neighbors' : False, # Parse relationships for States neighbor data.
        'entities.states.diplomacy' : False, # Parse relationships for States diplomacy data.
    'entities.states.diplomacy.all' : False, # Parse relationships for Neutral and Unknown diplomacies.
          'entities.states.history' : False, # Will parse history where appropriate 
               'entities.provinces' : False, # Parse Provinces
                   'entities.burgs' : False, # Parse Burgs
}
kanka_api = {
    'prefix' : 'https://kanka.io/api/1.0/',
    'token.filepath' : 'kanka.token',
    'campaignId' : '37130' # Test
}
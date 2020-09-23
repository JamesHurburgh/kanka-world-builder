options = {
                            'debug' : False,
                           'active' : False, # Will hit the Kanka api and create entities instead of just parsing them.
                         'heraldry' : False, # Will get heraldry from ironarachne.com and include in entities where appropriate 
                       'attributes' : False, # Will parse attributes on entities, not just the entities themselves.
                   'entities.world' : True, # This should always be true, otherwise many other things will fail.
               'entities.timelines' : True, # Parse Timelines
                  'entities.biomes' : True, # Parse Biomes
                  'entities.rivers' : True, # Parse Rivers
                  'entities.states' : True, # Parse States
        'entities.states.neighbors' : True, # Parse relationships for States neighbor data.
        'entities.states.diplomacy' : True, # Parse relationships for States diplomacy data.
    'entities.states.diplomacy.all' : False, # Parse relationships for Neutral and Unknown diplomacies.  Probably leave this off.
          'entities.states.history' : True, # Will parse history where appropriate 
               'entities.provinces' : True, # Parse Provinces
                   'entities.burgs' : False, # Parse Burgs
}
kanka_api = {
    'prefix' : 'https://kanka.io/api/1.0/',
    'token.filepath' : 'kanka.token',
    'campaignId' : '37130' # Test
}
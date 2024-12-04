
Locations = {"Tang Zheng Tang Chinese Pavilion" : "Find a building on water", 
             "Gym" : "Uncover SUTD's mewing hideout (translation: a place where you can work out)",
             "T-lab": "sugarcoated shop",
             "OneStop Centre" : "Go to our general office",
             "Albert Hong Lecture Theatre" : "Find a place where lessons are conducted",
             "Scrapyard" : "Locate the area to discard and reuse waste",
             "Swimming pool" : "An area with a lifeguard",
             "Fab-Lab" : "Go to the place where nothing becomes something",
             "Upper Changi MRT" : "Find our favourite transport mode",
             "D'Star Bistro": "Rediscover the area with western food",
             "Campus Centre" : "Unveil the region where fairs are usually performed (aka. Main lobby)",
             "Vending machines" : "Go to a place near the machinery systems that dispenses meals and drinks"}
items=list(Locations.items())
def choose_loc(Location_somewhere):
    import random
    x=random.randint(0,11)
    key, value = Location_somewhere[x]
    return key,value
from dotenv import load_dotenv
from time import sleep

# TODO remove IJSON dependency here
# TODO regenerate requirements.txt once dependencies tidied up.
import ijson

import os
import redis

load_dotenv()

# Connect to Redis
redis_client = redis.from_url(os.getenv("REDIS_URL"))

# Drop any existing index.
try:
    redis_client.ft("idx:regions").dropindex(delete_documents = False)
except:
    # Dropping an index that doesn't exist throws an exception 
    # but isn't an error in this case - we just want to start
    # from a known point.
    pass

# TODO CREATE NEW INDEX WITH GENERIC COMMAND APPROACH.
# Create a new index.
# ft.create idx:regions on json prefix 1 region: schema $.name as name tag $.boundaries as boundaries geoshape spherical $.forecast.wind as wind text $.forecast.sea as sea text $.forecast.weather as weather text $.forecast.visibility as visibility text 

# Load the shipping forecast regional data from the JSON file.
num_loaded = 0

with open ("data/shipping_forecast_regions.json", "rb") as input_file:
    jsonobj = ijson.items(input_file, "regions")
    objs = (o for o in jsonobj)

    for regions in objs:
        for region in regions:
            redis_key = f"region:{region['name'].replace(' ', '_').lower()}"
            redis_client.json().set(redis_key, "$", region)
            num_loaded += 1
            print(f"Stored {redis_key} ({region['name']})")

print(f"Regions loaded: {num_loaded}")

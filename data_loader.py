from dotenv import load_dotenv
from time import sleep

import json
import os
import redis

load_dotenv()

# Connect to Redis
redis_client = redis.from_url(os.getenv("REDIS_URL"))

# Drop any existing index.
try:
    print("Checking for previous index and dropping if found.")
    redis_client.ft("idx:regions").dropindex(delete_documents = False)
    print("Dropped old search index.")
except redis.exceptions.ResponseError as e:
    # Dropping an index that doesn't exist throws an exception 
    # but isn't an error in this case - we just want to start
    # from a known point.

    if not str(e).startswith("Unknown Index"):
        print("Error:")
        print(e)
        os._exit(1)

# Create a new index.
print("Creating index.")

redis_client.execute_command("FT.CREATE", "idx:regions", "ON", "JSON", "PREFIX", "1", "region:", "SCHEMA", "$.name", "AS", "name", "TAG", "$.boundaries", "AS", "boundaries", "GEOSHAPE", "SPHERICAL", "$.forecast.wind", "AS", "WIND", "TEXT", "$.forecast.sea", "AS", "sea", "TEXT", "$.forecast.weather", "AS", "weather", "TEXT", "$.forecast.visibility", "AS", "visibility", "TEXT")

# Load the shipping forecast regional data from the JSON file.
# TODO make filename configurable
num_loaded = 0

with open ("data/shipping_forecast_regions.json", "r") as input_file:
    file_data = json.load(input_file)

    for region in file_data["regions"]:
        redis_key = f"region:{region['name'].replace(' ', '_').lower()}"
        redis_client.json().set(redis_key, "$", region)
        num_loaded += 1
        print(f"Stored {redis_key} ({region['name']})")

redis_client.quit()

print(f"Regions loaded: {num_loaded}")
print("Done!")

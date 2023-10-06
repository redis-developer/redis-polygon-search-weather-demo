from dotenv import load_dotenv
from pathlib import Path
from time import sleep
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import TextField, TagField, GeoShapeField

import argparse
import json
import os
import redis

WEATHER_KEY_PREFIX = "region"
WEATHER_INDEX_NAME = "idx:regions"

load_dotenv()

# Parse arguments and make sure we were invoked correctly.
arg_parser = argparse.ArgumentParser(description = "Load JSON data into Redis for search demo.")
arg_parser.add_argument("--load", dest="data_file_name", required=True, help="File containing JSON data to load.")
args = arg_parser.parse_args()

# Check if the data file exists...
data_file_path = Path(args.data_file_name)

if not data_file_path.is_file():
    print(f"Data file {args.data_file_name} does not exist!")
    os._exit(1)

# Connect to Redis
redis_client = redis.from_url(os.getenv("REDIS_URL"))

# Drop any existing index.
try:
    print("Checking for previous index and dropping if found.")
    redis_client.ft(WEATHER_INDEX_NAME).dropindex(delete_documents = False)
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

redis_client.ft(WEATHER_INDEX_NAME).create_index(
    [
        TagField("$.name", as_name = "name"),
        GeoShapeField("$.boundaries", GeoShapeField.SPHERICAL, as_name = "boundaries"),
        TextField("$.forecast.wind", as_name = "wind"),
        TextField("$.forecast.sea", as_name = "sea"),
        TextField("$.forecast.weather", as_name = "weather"),
        TextField("$.forecast.visibility", as_name = "visibility")
    ],
    definition = IndexDefinition(
        index_type = IndexType.JSON,
        prefix = [ f"{WEATHER_KEY_PREFIX}:" ]
    )
)

# Load the shipping forecast regional data from the JSON file.
num_loaded = 0

with open (args.data_file_name, "r") as input_file:
    file_data = json.load(input_file)

    for region in file_data["regions"]:
        redis_key = f"{WEATHER_KEY_PREFIX}:{region['name'].replace(' ', '_').lower()}"
        redis_client.json().set(redis_key, "$", region)
        num_loaded += 1
        print(f"Stored {redis_key} ({region['name']})")

redis_client.quit()

print(f"Regions loaded: {num_loaded}")
print("Done!")

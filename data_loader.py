from dotenv import load_dotenv
from pathlib import Path
from time import sleep

import argparse
import json
import os
import redis

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
num_loaded = 0

with open (args.data_file_name, "r") as input_file:
    file_data = json.load(input_file)

    for region in file_data["regions"]:
        redis_key = f"region:{region['name'].replace(' ', '_').lower()}"
        redis_client.json().set(redis_key, "$", region)
        num_loaded += 1
        print(f"Stored {redis_key} ({region['name']})")

redis_client.quit()

print(f"Regions loaded: {num_loaded}")
print("Done!")

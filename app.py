from dotenv import load_dotenv
from flask import Flask, render_template, request
import os
import json
import redis

load_dotenv()

app = Flask(__name__)

# Connect to Redis
redis_client = redis.from_url(os.getenv("REDIS_URL"))

@app.route("/search", methods = ["POST"])
def search():
    wkt_string = ""
    geo_operator = ""

    # See if we got a point or a polygon search...
    if "point" in request.json:
        # Get the lat/lng and create a WKT point.
        wkt_string=f"POINT({request.json['point']['lng']} {request.json['point']['lat']})"
        geo_operator = "CONTAINS"
    else:
        # Unpack the GeoJSON request body and get the polygon out...
        # Create a WKT polygon.
        poly_coordinates = request.json["polygon"]["geometry"]["coordinates"][0]
        wkt_string = "POLYGON(("
        geo_operator = "WITHIN"

        for coords in poly_coordinates:
            wkt_string = f"{wkt_string}{coords[0]} {coords[1]},"

        wkt_string = f"{wkt_string[:-1]}))"

    # ft.search idx:regions "@boundaries:[WITHIN $poly]" PARAMS 2 poly 'POLYGON((-12.655691 61.48076, 0.176516 63.66576, 7.735213 59.265881, -12.655691 61.48076))' DIALECT 3 RETURN 1 name

    # ft.search idx:regions "@boundaries:[CONTAINS $poly]" PARAMS 2 poly 'POLYGON((-12.655691 61.48076, 0.176516 63.66576, 7.735213 59.265881, -12.655691 61.48076))' DIALECT 3 RETURN 1 name

    # Point in polygon... 55.128996, -1.159153
    # ft.search idx:regions "@boundaries:[CONTAINS $point]" PARAMS 2 point 'POINT(-1.159153 55.128996)' DIALECT 3 RETURN 1 name

    search_response = redis_client.execute_command(
        "FT.SEARCH", "idx:regions", f"@boundaries:[{geo_operator} $wkt]", "PARAMS", "2", "wkt", wkt_string, "DIALECT", "3", "LIMIT", "0", "100"
    )

    # TODO convert the polygon data into something more meaningful to the front end,
    # optimize the search above to only bring back fields/paths we need?

    matching_regions = []

    if search_response[0] > 0:
        for region_response in search_response[2::2]:
            region = json.loads(region_response[1])[0]
            matching_regions.append(region)

    return ({ 
        "data": matching_regions
    })

@app.route("/")
def home():
    return render_template('homepage.html')
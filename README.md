# Redis Stack Polygon Search Weather Demo

![Polygon search example in action](screenshots/polyweather.gif)

## Introduction

This repository is a small self-contained demonstration of the Polygon Search functionality that was added in the 7.2 release of Redis Stack.

For information about this release and the other new features in it, check out the [blog post](https://redis.com/blog/introducing-redis-7-2/).

Using data for the 31 regions of the British [Shipping Forecast](https://www.metoffice.gov.uk/weather/specialist-forecasts/coast-and-sea/shipping-forecast), we'll look at how to use the Search capability of Redis Stack to find which shipping forecast regions fall within an area described by a polygon, and also which shipping forecast region any given point around the British Isles belongs to.

This example uses the real Shipping Forecast regions, along with fixed text data for each that describes the four components of a forecast:

* Wind
* Sea State
* Weather
* Visibility

Check out the [Shipping Forecast on Wikipedia](https://en.wikipedia.org/wiki/Shipping_Forecast) for more information about this unique maritime weather broadcast.

## Prerequisites

You'll need to have the following installed:

* [Python](https://www.python.org/) - version 3.10 or higher.  We've tested this with Python 3.10.7.
* [Docker Desktop](https://www.docker.com/products/docker-desktop/).
* [Git command line tools](https://git-scm.com/downloads) to clone the repository (or if you don't have these, you can get a .zip file from GitHub instead).
* A browser (we've tested this with [Google Chrome](https://www.google.com/chrome/)).
* Optional but recommended: [RedisInsight](https://redis.io/docs/ui/insight/) - a graphical tool for viewing and managing data in Redis.

## Running the Demo

To run the demo, you'll need to clone the repository from GitHub, create a Python virtual environment then install the dependencies and start a Redis Stack instance.  We've provided a Docker Compose file for Redis Stack.  

Begin by cloning the repository from GitHub:

```
git clone https://github.com/redis-developer/redis-polygon-search-weather-demo.git
cd redis-polygon-search-weather-demo
```

Enter the following commands to create the virtual environment and install dependencies:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Now, start Redis Stack:

```
docker-compose up -d
```

We're using a `.env` file to store secrets such as the host and port that Redis runs on.  An example environment file `example.env` is included in this repository.

If you're using Redis Stack with the Docker Compose provided, you won't need to change any values, and can just copy `env.example` to `.env`:

```
cp env.example .env
```

If you need to change the Redis connection details (for example because your Redis Stack instance runs remotely or uses a password, or you want to change the port that the backend server runs on), edit `.env` accordingly before proceeding further.

The next step is to load the data into Redis Stack:

```
python data_loader.py --load data/shipping_forecast_regions.json
```

You should see output similar to this:

```
Checking for previous index and dropping if found.
Creating index.
Stored region:bailey (Bailey)
Stored region:biscay (Biscay)
Stored region:cromarty (Cromarty)
Stored region:dogger (Dogger)
Stored region:dover (Dover)
Stored region:faeroes (Faeroes)
Stored region:fair_isle (Fair Isle)
Stored region:fastnet (Fastnet)
Stored region:fisher (Fisher)
Stored region:fitzroy (Fitzroy)
Stored region:forth (Forth)
Stored region:forties (Forties)
Stored region:german_bight (German Bight)
Stored region:hebrides (Hebrides)
Stored region:humber (Humber)
Stored region:irish_sea (Irish Sea)
Stored region:lundy (Lundy)
Stored region:malin (Malin)
Stored region:north_utsire (North Utsire)
Stored region:plymouth (Plymouth)
Stored region:portland (Portland)
Stored region:rockall (Rockall)
Stored region:shannon (Shannon)
Stored region:sole (Sole)
Stored region:south_east_iceland (South East Iceland)
Stored region:south_utsire (South Utsire)
Stored region:thames (Thames)
Stored region:trafalgar (Trafalgar)
Stored region:tyne (Tyne)
Stored region:viking (Viking)
Stored region:wight (Wight)
Regions loaded: 31
Done!
```

Start the Flask server application:

```
flask run
```

You should see output similar to this:

```
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 253-334-353
```

Point your browser at `http://localhost:5000` and start clicking and dragging markers to create a polygon.  

TODO further instructions...

Use the "Reset" button to clear your polygon and any matching search results.

When you're finished using the demo, stop the Flask server using `Ctrl-C`, then turn off the Docker container like so:

```
docker-compose down
```

## Redis Data Model

Each region's data is stored as a JSON document using Redis Stack's JSON data type.

The Redis key for each document consists of the prefix `region:` and the region's name converted to lowercase and with `_` replacing spaces.

For example, the key for the "Irish Sea" region is `region:irish_sea`.

Using a prefix allows us to identify what sort of data might be stored at each key more easily, and also allows us to configure the search capablity of Redis Stack to only index that part of the keyspace.

Take a look at one of the keys using either RedisInsight or the Redis CLI.

Start the Redis CLI which will automatically connect to Redis at `localhost:6379` (our Docker container):

```
docker exec -it redis-polygon-search-
weather-demo redis-cli
```

Now use the [JSON.GET](https://redis.io/commands/json.get/) command to retrieve the document for the "Irish Sea" region:

```
127.0.0.1:6379> json.get region:irish_sea
"{\"name\":\"Irish Sea\",\"boundaries\":\"POLYGON((-6.328125 55.24155203565252,-5.888671875 55.32914440840507,-5.592041015625 55.29162848682989,-5.47119140625 55.70235509327093,-5.25146484375 55.85681658243853,-4.76806640625 55.64659898563683,-4.68017578125 55.441479359140686,-5.185546875 55.00282580979323,-5.240478515625 54.92714186454645,-4.94384765625 54.648412502316695,-4.844970703125 54.629338216555766,-4.954833984374999 54.813348417419284,-4.8779296875 54.84498993218758,-4.39453125 54.667477840945715,-4.306640625 54.84498993218758,-4.031982421875 54.74364976592378,-3.504638671875 54.95869417101661,-3.262939453125 54.95238569063361,-3.504638671875 54.749990970226925,-3.658447265625 54.533832507944304,-3.2299804687499996 54.06583577161278,-3.01025390625 54.17529672404642,-2.8784179687499996 54.181726602390945,-2.98828125 53.94315470224928,-3.065185546875 53.76170183021049,-2.98828125 53.73571574532637,-3.1201171874999996 53.585983654559804,-3.05419921875 53.4357192066942,-3.218994140625 53.37677497506021,-3.076171875 53.25206880589414,-3.394775390625 53.35710874569601,-3.7353515625 53.291489065300226,-3.856201171875 53.31774904749087,-4.075927734375 53.24549522839598,-4.317626953125 53.4357192066942,-4.537353515625 53.4291738804146,-4.63623046875 53.32431151982718,-4.350585937499999 53.12040528310657,-4.74609375 52.80940281068805,-4.19677734375 52.89564866211353,-4.04296875 52.5095347703273,-4.50439453125 52.16045455774706,-5.185546875 51.944264879028765,-6.328125 52.26815737376817,-6.448974609375 52.35547370875268,-6.185302734375 52.576349937498875,-6.218261718749999 52.65639394198803,-6.009521484375 52.96849212681396,-6.141357421875 53.291489065300226,-6.240234374999999 53.34399288223422,-6.064453125 53.533778184257805,-6.26220703125 53.67068019347264,-6.26220703125 53.78118084719588,-6.26220703125 53.85900655610469,-6.361083984374999 53.91081008725409,-6.35009765625 54.02713344412541,-6.141357421875 53.98839506479995,-5.9326171875 54.1173828217967,-5.888671875 54.220284882124005,-5.679931640625 54.23312964750767,-5.4931640625 54.39974815563759,-5.438232421875 54.48280455958253,-5.548095703125 54.648412502316695,-5.60302734375 54.69288437829768,-5.877685546874999 54.629338216555766,-5.679931640625 54.7943516039205,-5.789794921875 54.87660665410869,-5.965576171875 55.00912637001031,-5.9765625 55.07836723201515,-6.04248046875 55.10351605801967,-5.987548828125 55.17259379606185,-6.097412109375 55.23528803992295,-6.207275390625 55.20395325785898,-6.328125 55.24155203565252))\",\"forecast\":{\"wind\":\"West or northwest, backing southwest for a time, 3 to 5.\",\"sea\":\"Smooth or slight elsewhere.\",\"weather\":\"Showers, perhaps thundery later.\",\"visibility\":\"Good, occasionally poor.\"}}"
```

If you're using RedisInsight, start it up and add a new connection to Redis at `localhost` port `6379` with no user or password specified.  You can then browse the key space and see the data contained in each key.

You'll see that each region contains a JSON document with the following data items in it:

* `name`: The proper name for the region.
* `boundaries`: A [Well-known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) Polygon representation of the boundaries of the region.  These consist of a set of longitude/latitude co-ordinate pairs.  The first and last pair must be the same to "close" the polygon.  The search capability of Redis Stack uses the Well-known Text format to describe polygons and points.
* `forecast`: An object containing the following keys describing the four parts of a shipping forecase for the region:
  * `wind`: Description of the wind conditions.
  * `sea`: Description of the sea state.
  * `weather`: General overview of the weather.
  * `visibility`: Description of the visibility in the region.

If you'd like to see the raw data for all 31 regions, take a look at the [`data/shipping_forecast_regions.json`](data/shipping_forecast_regions.json) file.

## How does the Demo Work?

### Loading the Data and Creating an Index

TODO

### Serving a Map and Defining the Search Polygon

TODO

### TODO other sections...

TODO

## Questions / Ideas / Feedback?

If you have any questions about this, or fun ideas for how to use polygon search in your application we'd love to hear from you.  Find the Redis Developer Relations team and thousands of other Redis developers like you on the [official Redis Discord](https://discord.gg/redis).

If you find a bug please [raise an issue on GitHub](https://github.com/redis-developer/redis-polygon-search-weather-demo/issues) and we'll work to fix it.

## Additional Resources

If you'd like to learn more about the technologies and approaches used here, check out these links...

* [Redis Polygon Search Trains Demo](https://github.com/redis-developer/redis-polygon-search-trains-demo): another demo project that shows how to search for locations represented by points inside a search polygon.  This is written in Node.js.
* [RU204 Storing, Querying, and Indexing JSON at Speed](https://university.redis.com/courses/ru204/): a free online course at Redis University.
* The [redis-py client](https://github.com/redis/redis-py).
* [Search and Query in Redis Stack](https://redis.io/docs/interact/search-and-query/) (redis.io).
* The [`FT.CREATE`](https://redis.io/commands/ft.create/) command (redis.io).
* The [`FT.SEARCH`](https://redis.io/commands/ft.search/) command (redis.io).
* [Flask](https://flask.palletsprojects.com/): A web application framework for Python.
* The [Bulma CSS Framework](https://bulma.io/).
* [Leaflet](https://leafletjs.com/): A JavaScript library for interactive maps.
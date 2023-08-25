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

TODO

## How does the Demo Work?

### Loading the Data and Creating an Index

TODO

### Serving a Map and Defining the Search Polygon

TODO

### TODO other sections...

TODO

## Questions / Ideas / Feedback?

If you have any questions about this, or fun ideas for how to use polygon search in your application we'd love to hear from you.  Find the Redis Developer Relations team and thousands of other Redis developers like you on the [official Redis Discord](https://discord.gg/redis).

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
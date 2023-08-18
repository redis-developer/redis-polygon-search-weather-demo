from dotenv import load_dotenv
from flask import Flask, render_template
import os
import redis

load_dotenv()

app = Flask(__name__)

# Connect to Redis
redis_client = redis.from_url(os.getenv("REDIS_URL"))

@app.route("/")
def home():
    return render_template('homepage.html')
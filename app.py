from dotenv import load_dotenv
from flask import Flask, render_template
import redis

load_dotenv()

app = Flask(__name__)

# TODO connect to Redis

@app.route("/")
def home():
    return render_template('homepage.html')
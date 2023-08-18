from dotenv import load_dotenv
import os
import redis

load_dotenv()

# Connect to Redis
redis_client = redis.from_url(os.getenv("REDIS_URL"))
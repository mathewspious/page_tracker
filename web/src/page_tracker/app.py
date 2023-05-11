import os
from functools import cache
from flask import Flask
from redis import Redis, RedisError


app = Flask(__name__)
# replacing with def redis() to support mocking
#redis = Redis()

@app.get("/")
def index():
    try:
        page_views = redis().incr("page_views")
        return f"This page has been seen {page_views} times."
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{pensive face}", 500

@cache
def redis():
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

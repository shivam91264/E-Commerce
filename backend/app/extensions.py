# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
from flask_caching import Cache


cache = Cache(config={
    "CACHE_TYPE": "SimpleCache",  # memory cache (no Redis needed)
    "CACHE_DEFAULT_TIMEOUT": 60
})
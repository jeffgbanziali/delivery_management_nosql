import redis
from pymongo import MongoClient

# ── Redis ──────────────────────────────────────────────
REDIS_HOST = "localhost"
REDIS_PORT = 6379

def get_redis():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.ping()  # vérifie la connexion
    return r

# ── MongoDB ────────────────────────────────────────────
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB  = "delivery"

def get_mongo():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.server_info()  # vérifie la connexion
    return client[MONGO_DB]

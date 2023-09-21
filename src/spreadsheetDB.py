import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")


# if done locally, can use r = redis.Redis(host="localhost", port=6379)
r = redis.from_url(REDIS_URL, decode_responses=True)


def add_spreadsheet(server_id, spreadsheet_id):
    r.set(server_id, spreadsheet_id.encode('utf-8'))

def get_spreadsheet(server_id):
    return r.get(server_id)


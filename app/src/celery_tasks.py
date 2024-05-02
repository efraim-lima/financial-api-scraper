#Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from celery import Celery
from redis import Redis
from app.src.client import getQuote
from app.src.performance import scrape

app = Celery('tasks', broker='redis://localhost:6379/0')

# Initialize the Redis connection
redis_conn = redis.Redis(
    host='localhost', 
    port=6380,
    socket_timeout=5,
    password=os.getenv('REDIS_PASSWORD'),
    db=0
    )

@app.task
def stock(json_data):
    redis_conn.set('json_data', json.dumps(json_data))

@app.task
def scraper():
    while True:
        json_data = redis_conn.get(ticker)
        if json_data:
            json_data = json.loads(json_data)
            if 'stock_symbol' in json_data:
                # Do something with the json_data
                break


#celery -A tasks worker --loglevel=info

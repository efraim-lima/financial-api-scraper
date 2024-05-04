#Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from celery import Celery
import datetime
from dotenv import load_dotenv
import json
import redis
import app.src.client as client
import app.src.performance as performance
from app.logs.logs import info, error, warn, critic

load_dotenv()
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

password=os.getenv('REDIS_PASSWORD')
host=os.getenv('REDIS_HOST')
app = Celery('celery_tasks', broker=f'redis://:{password}@{host}:6380/0')
app.conf.result_backend = f'redis://:{password}@{host}:6380/0'

# Initialize the Redis connection
redis_conn = redis.Redis(
    host=f'{host}', 
    port=6380,
    socket_timeout=5,
    password=f'{password}',
    db=0
    )

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")


@app.task
def stock(stock_symbol):
    if redis_conn.exists(stock_symbol):
        json_data = redis_conn.get(stock_symbol)
        json_data = json.loads(json_data)

        warn(f"stock cache for {stock_symbol} accessed at {now}")
        return json_data
    else:
        json_data = client.getQuote(stock_symbol)
        redis_conn.set(stock_symbol, json.dumps(json_data))
        warn(f"{stock_symbol} accessed in stock api at {now}")

        # Set TTL for the key
        redis_conn.expire(stock_symbol, 5 * 24 * 60 * 60)
        results = json.dumps(json_data)
        return results

@app.task
def scraper(stock_symbol):
    if redis_conn.exists(stock_symbol):   
        json_data = redis_conn.get(stock_symbol)
        json_data = json.loads(json_data)
        if 'performance' in json_data:
            warn(f"scraper cache for {stock_symbol} accessed at {now}")

            # Save the updated data back to Redis
            redis_conn.set(stock_symbol, json.dumps(json_data))
            return json.dumps(json_data)
        else:
            result = performance.scrape(stock_symbol, json_data)
            redis_conn.set(stock_symbol, json.dumps(result))
            warn(f"{stock_symbol} accessed in scraper api at {now}")
            return json.dumps(result)
@app.task
def validate(stock_symbol):
    if redis_conn.get(stock_symbol) == None:
        return True

#celery -A tasks worker --loglevel=info

#Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from celery import Celery
import json
import redis
import app.src.client as client
import app.src.performance as performance

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

@app.task
def stock(stock_symbol):
    if redis_conn.exists(stock_symbol):
        json_data = json.loads(json_data)
        
        print(f"\n\n\n CACHEEEEEEEE \n\n\n")
        return json_data
    else:
        json_data = client.getQuote(stock_symbol)
        redis_conn.set(stock_symbol, json.dumps(json_data))
        print(f"\n\n\n NÃO CACHE \n\n\n")
        # Set TTL for the key
        redis_conn.expire(stock_symbol, 5 * 24 * 60 * 60)
        print(f"\nstock result\n\n{json_data}\n")
        print(type(json_data))
        results = json.dumps(json_data)
        return results

@app.task
def scraper(stock_symbol):
    if redis_conn.exists(stock_symbol):   
        print("\n\n\n JSON DATA OK \n\n\n") 
        json_data = json.loads(json_data)
        if 'performance' in json_data:
            print("\n\n\n\n CACHEEEEEEEEE22222222")
            # Save the updated data back to Redis
            redis_conn.set(stock_symbol, json.dumps(json_data))

            # # Set TTL for the key if it doesn't already have one
            # if redis_conn.pttl(stock_symbol) == -1:
            #     redis_conn.expire(stock_symbol, 5 * 24 * 60 * 60)
            print(f"\nscraper result\n\n{result}")
            print(type(result))
            return json.dumps(json_data)
        else:
            result = performance.scrape(stock_symbol, json_data)
            redis_conn.set(stock_symbol, json.dumps(result))
            print(f"\nscraper result\n\n{result}")
            print(type(result))
            return json.dumps(result)
@app.task
def validate(stock_symbol):
    if redis_conn.get(stock_symbol) == None:
        return True

#celery -A tasks worker --loglevel=info

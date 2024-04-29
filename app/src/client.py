import os
polygonKey = os.environ.get("POLYGON_API_KEY")

import datetime
import holidays
import json
from polygon import RESTClient
import redis
import requests

#maybe in some cases we need to export environment variables
# $ export POLYGON_API_KEY="mqJl50msy2bOXpEVFjgNeYpCbsu0zo3f"

# Here we get the API_KEY that was saved in the environment variable
redis_conn = redis.StrictRedis(
    host='localhost', 
    port=6379,
    decode_responses=True,
    db=0
)
today = datetime.date.today()

def is_business_day(date):
    # Check if the day is a weekday (Monday=0, Sunday=6)
    if date.weekday() < 5:
        # Check if the day is not a public holiday
        if date not in holidays.CountryHoliday('USA'):
            return True
    return False

def last_business_day(date):
    prev_day = date - datetime.timedelta(days=1)
    while not is_business_day(prev_day):
        prev_day -= datetime.timedelta(days=1)
    return prev_day

if is_business_day(today):
    day = today.strftime('%Y-%m-%d')
else:
    last_bd = last_business_day(today)
    day = last_bd.strftime('%Y-%m-%d')

def getQuote(ticker):
    poligonKey="mqJl50msy2bOXpEVFjgNeYpCbsu0zo3f"
    response = requests.get(f"https://api.polygon.io/v1/open-close/{ticker}/{day}?apiKey={polygonKey}")
    if response.status_code == 200:
        data = response.json()
        data = json.dumps(data)
        try:
            if redis_conn.exists(ticker):
                # TODO: check the reddis connection and api return
                # Key exists, so merge the data
                performance_data = redis_conn.hget(ticker, "performance")
                if performance_data is not None:
                    json_data = json.loads(performance_data)
                    new_data = {**data, **json_data}
                    redis_conn.hset(ticker, "performance", json.dumps(new_data))
                else:
                    # Update the data in the cache
                    redis_conn.hset(ticker, "performance", json.dumps(data))
            else:
                # Key does not exist, so store the data
                redis_conn.hset(ticker, mapping=data)
            redis_conn.setex(stock_symbol, 60, quote)
        except Exception as e:
            print(e)
        redis_conn.setex(ticker, 5*24*60*60, data)

        return data
    else:
        print(response.status_code)
        print(response.text)
        return None

def getTickers():
    response = requests.get(f"https://api.polygon.io/v3/reference/tickers?active=true&apiKey={polygonKey}")
    if response.status_code == 200:
        data = response.json()
        try:
            quote = json.dumps(quote)
            redis_conn.setex(stock_symbol, 60, quote)
            return data
        except Exception as e:
            print(e)
        redis_conn.setex("tickers", 5*24*60*60, json.dumps(data))
        return data
    else:
        print(response.status_code)
        print(response.text)
        return None


#second way to get data:
"""
def getQuote(ticker):
    client = RESTClient(api_key=polygonKey)
    quote = client.get_daily_open_close_agg(ticker, day)
    redis_conn.set(ticker, json.dumps(quote), ex=30)
    print(quote)
    return quote
"""
getQuote("AAPL")
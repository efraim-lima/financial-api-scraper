import os
polygonKey = os.environ.get("POLYGON_API_KEY")

import calendar
import datetime
import holidays
import json
from polygon import RESTClient
import redis
import requests

#maybe in some cases we need to export environment variables
# $ export POLYGON_API_KEY="mqJl50msy2bOXpEVFjgNeYpCbsu0zo3f"

# Here we get the API_KEY that was saved in the environment variable
redis_conn = redis.Redis(
    host='127.0.0.1', 
    port=6379,
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

today = datetime.date.today()

if is_business_day(today):
    if today.weekday() == calendar.MONDAY:
        last_bd = last_business_day(today)
        day = last_bd.strftime('%Y-%m-%d')
        print(f"The last business before Monday was: {day}")
    else:
        last_bd = last_business_day(today)
        day = last_bd.strftime('%Y-%m-%d')
        print(f"The last business before today was: {day}")
else:
    last_bd = last_business_day(today)
    day = last_bd.strftime('%Y-%m-%d')
    print(f"The last business day before today was: {day}")

def getQuote(ticker):
    poligonKey="mqJl50msy2bOXpEVFjgNeYpCbsu0zo3f"
    response = requests.get(f"https://api.polygon.io/v1/open-close/{ticker}/{day}?apiKey={polygonKey}")
    if response.status_code == 200:
        data = response.json()
        data = json.dumps(data)
        data = response.json()

        try:
            # Check if the key exists in Redis
            if not redis_conn.exists(ticker) or redis_conn.type(ticker) != 'string':
                redis_conn.set(ticker, json.dumps(data))
            else:
                # Key exists, so update the data
                existing_data = json.loads(redis_conn.get(ticker))
                existing_data.update(data)
                redis_conn.set(ticker, json.dumps(existing_data))

            # Set TTL for the key
            redis_conn.expire(ticker, 5 * 24 * 60 * 60)

        except Exception as e:
            print(e)
        print(data)
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
import os
polygonKey = os.environ.get("POLYGON_API_KEY")

import calendar
import datetime
from dotenv import load_dotenv
import holidays
import json
from polygon import RESTClient
import requests

load_dotenv()

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
    polygonKey=os.getenv('OBFUSCATE')
    response = requests.get(f"https://api.polygon.io/v1/open-close/{ticker}/{day}?apiKey={polygonKey}")
    if response.status_code == 200:
        # data = response.json()
        # data = json.dumps(data)
        data = response.json()
        print(f"\nQuote result\n\n{data}")
        print(type(data))
        return data
    else:
        print(response.status_code)
        print(response.text)
        return None
from bs4 import BeautifulSoup
import json
from lxml import html
import redis
from zenrows import ZenRowsClient
import zenrows

def scrape(ticker):
     # Initialize the Redis connection
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    
    ticker_l = ticker.lower()
    # Connect to the website and get the HTML content
        
    client = ZenRowsClient("c3ec573271fab14207b25f7da0b65a980a376e70")
    url = f"https://www.marketwatch.com/investing/stock/{ticker_l}"
    params = {"js_render":"true","json_response":"true","premium_proxy":"true"}
    response = client.get(url, params=params)

    response = response.text

    soup = BeautifulSoup(response, 'html.parser')

    import re
    pattern = re.compile(r'\d+\.\d+%')
    lis = soup.find_all('li', string=pattern)
    
    data = {
        "Ticker": ticker,
        "5 days": lis[0].get_text(),
        "1 Month": lis[1].get_text(),
        "3 Months": lis[2].get_text(),
        "Year to Date": lis[3].get_text(),
        "1 Year": lis[4].get_text()
    }
    print(data)
   # Check if the key exists in the cache
    if redis_conn.exists(ticker):
        # Key exists, so merge the data
        performance_data = redis_conn.hget(ticker, "performance")
        if performance_data is not None:
            json_data = json.loads(performance_data)
            json_data["performance"] = data
            redis_conn.hset(ticker, "performance", json.dumps(json_data))
        # Update the data in the cache
        redis_conn.hset(ticker, "performance", json.dumps(data))
    else:
        # Key does not exist, so store the data
        redis_conn.hset(ticker, mapping=data)

    json_data = json.dumps(data)
    return json_data

scrape("AAPL")
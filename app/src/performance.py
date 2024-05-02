from bs4 import BeautifulSoup
from dotenv import load_dotenv
from celery_tasks import scraper, stock
import json
from lxml import html
import redis
from zenrows import ZenRowsClient
import zenrows

load_dotenv()

# Initialize the Redis connection
redis_conn = redis.Redis(
    host='localhost', 
    port=6380,
    socket_timeout=5,
    password=os.getenv('REDIS_PASSWORD'),
    db=0
    )

def scrape(ticker):
    try:
        while True:
            json_data = redis_conn.get(ticker)
            if json_data:
                json_data = json.loads(json_data)
                if 'symbol' in json_data: 
                    # Do something with the json_data
                    ticker_l = ticker.lower()
                    # Connect to the website and get the HTML content
                    zenRowKey=os.getenv('OBFUSCATEII')
                    client = ZenRowsClient(zenRowKey)
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
                        "type": 1,
                        "5 days": lis[0].get_text(),
                        "1 Month": lis[1].get_text(),
                        "3 Months": lis[2].get_text(),
                        "Year to Date": lis[3].get_text(),
                        "1 Year": lis[4].get_text()
                    }

                    #appending json data with performance data
                    new_data = {**json_data, **data}
                    # Save the updated data back to Redis
                    redis_conn.set(ticker, json.dumps(new_data))
                    # Set TTL for the key
                    redis_conn.expire(ticker, 5 * 24 * 60 * 60)
                    break
    except (requests.exceptions.RequestException, redis.exceptions.RedisError) as e:
        print(f"Error: {e}")
    print(json_data)
    return json_data
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
from lxml import html
import redis
from zenrows import ZenRowsClient
import zenrows

load_dotenv()

def scrape(ticker):
    try:
        # Initialize the Redis connection
        redis_conn = redis.Redis(
            host='172.18.0.10', 
            port=6380,
            socket_timeout=5,
            #password=os.getenv('REDIS_PASSWORD'),
            db=0
            )
        
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
            "5 days": lis[0].get_text(),
            "1 Month": lis[1].get_text(),
            "3 Months": lis[2].get_text(),
            "Year to Date": lis[3].get_text(),
            "1 Year": lis[4].get_text()
        }
        json_data = json.dumps(data)

        # Check if the key exists in Redis
        if redis_conn.exists(ticker):
            # Key exists, get the cached data
            performance_data = redis_conn.get(ticker)
            if performance_data is not None:
                # Decode bytes to string and load JSON
                performance_data = performance_data.decode('utf-8')
                existing_data = json.loads(performance_data)
                # Update the existing data with new data
                new_data = {**existing_data, **data}
                # Save the updated data back to Redis
                redis_conn.set(ticker, json.dumps(new_data))
        else:
            # Key doesn't exist, save the new data to Redis
            redis_conn.set(ticker, json.dumps(data_json))

        # Set TTL for the key
        redis_conn.expire(ticker, 5 * 24 * 60 * 60)

    except (requests.exceptions.RequestException, redis.exceptions.RedisError) as e:
        print(f"Error: {e}")
    print(json_data)
    return json_data
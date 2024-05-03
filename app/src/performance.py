import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
from lxml import html
import redis
from zenrows import ZenRowsClient
import zenrows

load_dotenv()

def scrape(ticker, json_data):
    # json_data = json.loads(json_data)
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
        "performance": "performance",
        "5 days": lis[0].get_text(),
        "1 Month": lis[1].get_text(),
        "3 Months": lis[2].get_text(),
        "Year to Date": lis[3].get_text(),
        "1 Year": lis[4].get_text()
    }

    #appending json data with performance data
    new_data = {**json_data, **data}
    print(f"\nperformance result\n\n{new_data}")
    print(type(new_data))
    return json.dumps(new_data)
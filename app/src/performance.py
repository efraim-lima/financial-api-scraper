import requests
import json

def scrape(ticker):
    url=f"https://www.marketwatch.com/investing/stock/{ticker}"
    response=requests.get(url)

    fiveDays=html.get.xpath()
    oneMonth=html.get.xpath()
    threeMonths=html.get.xpath()
    YTD=html.get.xpath()
    oneYear=html.get.xpath()

    # TODO: save the data in sqlite

    data = {
        "Ticker":ticker,
        "5 days":fiveDays,
        "1 Month":oneMonth,
        "3 Months":threeMonths,
        "Year to Date":YTD,
        "1 Year":oneYear
    }

    json_data=json.dumps(data)
    return json_data
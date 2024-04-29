import random
import redis
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import ssldump
import undetected_chromedriver as uc

def scrape(ticker):
    # Initialize WebDriver with the proxy
    chrome_options = webdriver.ChromeOptions()
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.add_argument('-profile')
    options.add_argument(profile.path)

    # Set up the SSL dump options and generate a random TLS fingerprint
    ssl_options = ssldump.Session(ssl_version=ssldump.Version.TLS1_2, ciphers=ssldump.Ciphers.ALL,
                                   random_bytes=bytes.fromhex(random.randint(0, 2**128).to_bytes(32, 'big').hex()))

    # Set up the headers with a random user agent
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(USER_AGENTS)
    }

    # Set up the WebDriver with the SSL dump options and headers
    chrome_options.add_argument('--proxy-server=%s' % proxy)
    chrome_options.add_argument('--ssl-client-config-name=%s' % ssl_options.name)
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--remote-debugging-address=0.0.0.0')
    chrome_options.add_argument('--remote-debugging-ws-address=ws://0.0.0.0:9222')
    chrome_options.add_argument('--disable-features=NetworkService')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-gpu-shader-disk-cache')
    chrome_options.add_argument('--disable-accelerated-2d-canvas')
    chrome_options.add_argument('--disable-accelerated-jpeg-decoding')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--user-agent=%s' % headers['User-Agent'])

    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Initialize the Redis connection
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)

    ticker_l = ticker.lower()
    print(ticker_l)

    # Set up the Selenium driver with JavaScript enabled
    capabilities = DesiredCapabilities.CHROME
    capabilities["javascriptEnabled"] = True
    driver = webdriver.Chrome(desired_capabilities=capabilities)

    # Navigate to the website
    url = f"https://www.marketwatch.com/investing/stock/{ticker_l}"
    driver.get(url)

    print(driver.title)

    # Extract the required data
    fiveDays = extract_data(driver, '//*[@id="maincontent"]/div[6]/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[2]/ul/li[1]')
    oneMonth = extract_data(driver, '//*[@id="maincontent"]/div[6]/div[1]/div[2]/div[1]/table/tbody/tr[2]/td[2]/ul/li[1]')
    threeMonths = extract_data(driver, '//*[@id="maincontent"]/div[6]/div[1]/div[2]/div[1]/table/tbody/tr[3]/td[2]/ul/li[1]')
    YTD = extract_data(driver, '//*[@id="maincontent"]/div[6]/div[1]/div[2]/div[1]/table/tbody/tr[4]/td[2]/ul/li[1]')
    oneYear = extract_data(driver, '//*[@id="maincontent"]/div[6]/div[1]/div[2]/div[1]/table/tbody/tr[5]/td[2]/ul/li[1]')

    data = {
        "Ticker": ticker,
        "5 days": fiveDays,
        "1 Month": oneMonth,
        "3 Months": threeMonths,
        "Year to Date": YTD,
        "1 Year": oneYear
    }

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
    driver.quit() # Close the driver
    return json_data

scrape("AAPL")

def extract_data(driver, xpath):
    try:
        element = driver.find_element_by_xpath(xpath)
        if element:
            return element.text.strip()
        else:
            return ""
    except:
        return ""

def filter_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_links = soup.find_all('a', href=True)
    print(f'There are {len(all_links)} total links')
    visible_links = [link for link in all_links if is_visible(link)]
    print(f'There are {len(visible_links)} visible links')

def is_visible(link):
    link_style = link.get('style')
    if link_style is None:
        link_style = ''
    display = 'none' not in link_style
    visibility = 'hidden' not in link_style
    return display and visibility

def AAPLfingerprint():
    # Generate a random 20-byte value for the TLS fingerprint
    fingerprint = bytes.fromhex(random.randint(0, 2**128).to_bytes(32, 'big').hex())
    # Set the TLS fingerprint in the SSL dump options
    ssl_options = ssldump.Session(ssl_version=ssldump.Version.TLS1_2, ciphers=ssldump.Ciphers.ALL,
                                   random_bytes=fingerprint)
    return ssl_options

def headers(user_agent=None):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    if user_agent is not None:
        headers['User-Agent'] = user_agent
    return headers

def uc_browser(screen_size=(1920, 1080), resolution=(1920, 1080), font_dirs=None):
    # Create a headless Chrome browser instance
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(f'--window-size={screen_size[0]},{screen_size[1]}')
    options.add_argument('--force-device-scale-factor=1')
    options.add_argument(f'--device-pixel-ratio={screen_size[0] / resolution[0]}')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--remote-debugging-address=0.0.0.0')
    options.add_argument('--remote-debugging-ws-address=ws://0.0.0.0:9222')
    
    if font_dirs is not None:
        options.add_argument(f'--font-dirs={",".join(font_dirs)}')
    
    browser = uc.Chrome(options=options)
    return browser
# Flask API Application with Scraper Integration

This Flask API application is designed to provide users with stock data and the ability to "buy" stocks via API requests. Additionally, it incorporates a scraper to gather additional data from external sources for stock modeling purposes.

Main libs Used

bleach 💧

    HTML Sanitization: A library that helps remove malicious HTML tags and attributes from a given HTML document.

celery 🕒

    Task Queue: A distributed task queue that allows you to run tasks asynchronously, making your application more scalable and efficient.



Flask 🏠

    Web Framework: A lightweight web framework for Python that allows you to build web applications quickly and efficiently.


polygon-api-client 📊

    Financial Data: A Python library that provides access to financial data from Polygon, allowing you to fetch and analyze financial data.


redis 💻

    In-Memory Data Store: An in-memory data store that allows you to store and retrieve data quickly and efficiently.

requests 📊

    HTTP Requests: A library that allows you to send HTTP requests and interact with web servers, making it easy to fetch data from APIs.

Other libs used in this project:
appdirs 📁
beautifulsoup4 📊
build 🛠️
bs4 📊
holidays 📆
lxml 📊
numpy 📊
pip-tools 📦
requests_html 📊

    HTML Parsing: A library that allows you to parse HTML and interact with web pages, making it easy to scrape data from web pages.

zenrows 📊

    Data Analysis: A library that provides tools for data analysis, making it easy to work with and manipulate data.

python-dotenv 📁
setuptools 🛠️
urllib3 📊

## Functionality 🛠️

### a. Data Collection and Storage 📊

- Stock data is collected from APIs and stored in cache as JSON format.
- The scraper correlates stock tickers and retrieves data from another website, saving the data in cache and correlating it with stock symbols.

### b. Stock Purchase 💰

- Users can make stock purchases via POST requests to `/stock/<stock_symbol>`.
- Purchases are saved in an SQLite database for storage and further processing.

### c. Stock Information Retrieval 📈

- Users can retrieve stock information via GET requests to `/stock/<stock_symbol>`.
- Retrieved data is stored in a Redis cache for a short duration.
- The scraper enhances the stock data with performance data and appends it to the ticker JSON data. If the ticker doesn't exist, it creates a new entry.

### d. Frontend Interface 🖥️

- Users can access more information and select suggested stocks via the `stocks.html` frontend page.
- All processes are performed in the frontend with API connections.

### e. Deployment 🚀

- The application can be easily deployed using Docker Compose by running `docker-compose up -d` in the /root directory.

    ```bash
    docker-compose up -d
    ```
- I, particularly preffer run these commands:

    ```bash
    docker-compose down

    echo "y" | docker system prune -f && exit
    
    docker-composea up --build
     ```
- Requests can be made via browser client or CLI. For CLI usage, the following commands can be used:

    ```bash
    curl -X GET http://localhost:8000/stock/<stock_symbol>
    
    curl -X POST -H "Content-Type: application/json" -d '{"amount": <integer>}' http://localhost:8000/stock/<stock_symbol>
    ```

## Security Measures 🔒

- The code includes input and output sanitization to prevent code and SQL injection. Output escaping logic can be added for enhanced protection.

## Notes 📝

- While the code performs better in CLI mode, efforts are underway to develop a frontend solution.
- For any inquiries or assistance, feel free to contact Efraim Lima at efraim.alima@gmail.com or connect via [LinkedIn](https://linkedin.com/in/efraimlima).

## Feedback and Contributions 🙌

Your feedback and contributions to this project are highly appreciated. If you have any suggestions or want to contribute, please reach out to Efraim Lima.
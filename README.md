# Flask API Application with Scraper Integration

Hey there! Welcome to this README, where I'll walk you through our Flask API application with scraper integration. It's designed not only provide stock data but allows you to "buy" stocks via API requests.

## Main Libraries Used

Here are some of the main libraries I used in project:

- **bleach 💧**: Helps keep the SQL clean and free from any malicious injections, sanityzing it.
- **celery 🕒**: Powers task queue, ensuring asynchronous task execution for better scalability.
- **flask 🏠**: The web framework for build the API
- **logging 🛠️**: Keeps track of user activities, generating alerts and info as needed.
- **polygon-api-client 📊**: Provides access to financial data from Polygon.
- **redis 💻**: Used for cache management and messaging queue.
- **requests 📊**: Used for fetching data from web (APIs and Pages).
- **requests_html 📊**: Enables HTML parsing and web scraping for data extraction.
- **zenrows 📊**: An incredible tool for bypass scraping problems.

## Additional Libraries

I also used other helpful libraries like appdirs, beautifulsoup4, holidays, and numpy, among others.

## Functionality 🛠️

### Data Collection and Storage 📊

This tool collect stock data from APIs and store it in cache as JSON format. Ater this, the scraper correlates stock tickers and fetch additional data from external sources.

### Stock Purchase 💰

Users can easily make stock purchases through simple POST requests to `/stock/<stock_symbol>`. These purchases are then stored in an SQLite database for further processing.

```bash
curl -X POST -H "Content-Type: application/json" -d '{"amount": <integer>}' http://localhost:8000/stock/<stock_symbol>
```

After sending a POST request, you can access the database by following these steps:

- First, get the Docker container ID from app-test_app in docker ps:

```bash
docker ps
```

- Insert it into the command below to access the container shell:

```bash
docker exec -it <container_id> /bin/bash
```

- Finally, retrieve the database:

```bash
sqlite3 app/db/purchases.db

select * from history
```

### Stock Information Retrieval 📈

Users can retrieve stock information via GET requests to `/stock/<stock_symbol>`. The retrieved data is stored temporarily in a Redis cache and scraper get performance metrics, appending it to the ticker JSON response.

```bash
curl -X GET http://localhost:8000/stock/<stock_symbol>
```

### Frontend Interface 🖥️

I am currently working on a frontend interface (`stocks.html`) where users can access more information and select suggested stocks. All processes are integrated with API connections.

### Deployment 🚀

Deploying our application is easy! Just fire up Docker Compose with `docker-compose up -d` in the `/root` directory. 

```bash
docker-compose up -d
```

Personally, I prefer running these commands:

```bash

docker-compose down

echo "y" | docker system prune -f && exit

docker-compose up --build
```

### Security Measures 🔒

Security is my goal! My code includes input and output sanitization to prevent any potential code or SQL injection attacks. I'm also considering adding output escaping logic for additional protection.

### Notes 📝

While the code don't performs admirably in CLI mode, I am actively working on developing a user-friendly frontend solution. Stay tuned for updates!

### Feedback and Contributions 🙌

Your feedback and contribution mean too much for me! If you have any suggestions or want to contribute, don't hesitate to reach out to me (Efraim Lima). You can contact me via email at efraim.alima@gmail.com or connect on [LinkedIn](https://linkedin.com/in/efraimlima).

Thanks a lot for the opportunity!
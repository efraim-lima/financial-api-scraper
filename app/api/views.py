#Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, jsonify, render_template
from app.db import db
from app.src.celery_tasks import stock, scraper
import datetime
from dotenv import load_dotenv
import json
import redis
import sqlite3

load_dotenv()

app = Flask(__name__)
redis_conn = redis.Redis(
    host='localhost', 
    port=6380,
    socket_timeout=5,
    password=os.getenv('REDIS_PASSWORD'),
    )

def getStock(stock_symbol):
    quote = stock.delay(stock_symbol)
    result = quote.get()
    result = json.dumps(result)
    return jsonify(result)

def configure(app):
    @app.route('/')
    def stocks():
        return render_template(
            'index.html',
            title="Stocks")
    
    @app.route('/stock')
    def hello():
        return 'For now is just a view, but soon it will be a complete page with stocks for buy \n'

    @app.route('/stock/<string:stock_symbol>', methods=['GET'])
    def get_stock(stock_symbol):
        try:
            if redis_conn.get(stock_symbol) is None:
                quote = getStock(stock_symbol)
                
                quote = json.dumps(quote)
                scrape = scrape.delay(stock_symbol)
                
                result = scrape.get()
                result = json.dumps(result)
                # redis_conn.setex(stock_symbol, 60, quote)    
                return jsonify(result)
        except (requests.exceptions.RequestException, redis.exceptions.RedisError) as e:
            print(f"Error: {e}")
            return jsonify(json.loads(redis_conn.get(stock_symbol)))

    @app.route('/stock/<string:stock_symbol>', methods=['POST'])
    def purchase(stock_symbol):
        amount = request.json.get('amount')

        stock_symbol = stock_symbol.upper()

        # Get the current date and time
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        if not amount:
            abort(400, 'Invalid amount')
        
        conn = db.get_db()
        cursor = conn.cursor()
        db.insert(conn, stock_symbol, amount, now)

        if db.check(conn, stock_symbol, now) == True:
            quota = redis_conn.get(stock_symbol)
            quota = json.loads(quota)

            # Get the sum of all amounts for the given stock symbol
            amount_sum = db.get_amount_sum(conn, stock_symbol)
            # Add the amount sum to the quota JSON object
            quota['amount_sum'] = amount_sum

            phrase = f"{amount} units of stock {stock_symbol} were added to your stock record"
            return make_response(jsonify(phrase), 201)
        
        db.close()


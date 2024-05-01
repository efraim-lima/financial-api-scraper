#Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, jsonify, render_template
from app.db import db
from app.src.client import getQuote
import datetime
from dotenv import load_dotenv
import json
import redis
import sqlite3

load_dotenv()

app = Flask(__name__)
redis_conn = redis.Redis(
    host='172.18.0.10', 
    port=6380,
    socket_timeout=5,
    password=os.getenv('REDIS_PASSWORD'),
    )

def getStock(stock_symbol):
    quote = getQuote(stock_symbol)
    quote = json.dumps(quote)
    return quote

def configure(app):
    @app.route('/')
    def stocks():
        return render_template(
            'index.html',
            title="Stocks")
    
    @app.route('/stock')
    def hello():
        return 'Hello, World!'

    @app.route('/stock/<string:stock_symbol>', methods=['GET'])
    def get_stock(stock_symbol):
        try:
            if redis_conn.get(stock_symbol) is None:
                quote = getStock(stock_symbol)
                quote = json.dumps(quote)
                redis_conn.setex(stock_symbol, 60, quote)
        except (requests.exceptions.RequestException, redis.exceptions.RedisError) as e:
            print(f"Error: {e}")
        return jsonify(json.loads(redis_conn.get(stock_symbol)))

    @app.route('/stock/<string:stock_symbol>', methods=['POST'])
    def update_stock(stock_symbol):
        amount = request.json.get('amount')

        stock_symbol = stock_symbol.upper()

        # Get the current date and time
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        if not amount:
            abort(400, 'Invalid amount')
        
        conn = db.get_db()
        cursor = conn.cursor()
        
        if db.check(conn, stock_symbol, now) == False:
            db.insert(conn, stock_symbol, amount, now)

        db.close()

        return make_response(jsonify(f"{amount} stocks of {stock_symbol} purchased!"), 200)

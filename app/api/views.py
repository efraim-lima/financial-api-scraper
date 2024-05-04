#Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, request, jsonify, render_template, make_response
from app.db import db
from app.src.tasks import stock, scraper, validate
import datetime
from dotenv import load_dotenv
import json
import sqlite3

load_dotenv()

def getStock(stock_symbol):
    quote = stock.delay(stock_symbol)
    result = quote.get()

    result = json.dumps(result)
    print(f"\ngetStock result\n\n{result}")
    print(type(result))
    return result

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
        quote = getStock(stock_symbol)
        
        quote = json.loads(quote)
       
        print(f"\nget stock result\n\n{quote}")
        print(type(quote))
        scrape = scraper.delay(stock_symbol)
        
        result = scrape.get()
        result = json.loads(result) 
        
        print(f"\nget scrape result\n\n{result}")
        print(type(result))
        return jsonify(result)

    @app.route('/stock/<string:stock_symbol>', methods=['POST'])
    def purchase(stock_symbol):
        amount = str(request.json.get('amount'))
        if not amount:
            abort(400, 'Invalid amount')
        else:
            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            stock_symbol = stock_symbol.upper()
            conn = db.get_db_connection()
            db.insert(stock_symbol, amount, now)

            if db.check(stock_symbol, now) == True:
                # Get the sum of all amounts for the given stock symbol
                amount_sum = db.get_amount_sum(stock_symbol)

            phrase = f"{amount} units of stock {stock_symbol} were added to your stock record"
            db.close()
            return make_response(jsonify(phrase), 201)            


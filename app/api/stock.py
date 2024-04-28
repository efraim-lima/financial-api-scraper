from flask import Blueprint, render_template, request, abort, current_app
from app.src.client import getQuote
import redis
import json

bp = Blueprint('stocks', __name__, url_prefix='/stock')
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

def getStock(stock_symbol):
    quote = getQuote(ticker)
    symbol = quote['symbol']
    if not ticker:
        abort(400, 'Missing "ticker" parameter')
    return symbol, quote

@bp.route('/stock', methods=['GET','POST'])
def stocks():
    if request.method == 'GET':
        ticker = request.args.get('stock_symbol')
        if redis_conn.get(ticker) == None:
            symbol, quote = getStock(stock_symbol)
            redis_conn.set(symbol, json.dumps(stock), ex=30)
            return quote, render_template('stock.html')
    elif request.method == 'POST':
        amount = request.args.get('amount')
        stock_symbol = request.args.get('stock_symbol')
        if not amount or not stock_symbol:
            abort(400, 'Invalid amount or code')
        else:
            # TODO: save the amount, ticker and date in sqlite database that are configured in /app/db/db.py in function purchase()
            #return render_template('purchase.html', ticker=ticker, amount=amount)
            return jsonify({'message':f"{amount} of units purchased"})

@bp.route('/stock/<string:stock_symbol>', methods=['GET'])
def specificStock(stock_symbol):
    if redis_conn.get(stock_symbol) == None:
        symbol, stock = getStock(stock_symbol)
        redis_conn.set(symbol, json.dumps(stock), ex=30)
    return jsonify(stock)
    #return render_template('stock.html', ticker=ticker)

def configure(app):
    app.register_blueprint(bp)

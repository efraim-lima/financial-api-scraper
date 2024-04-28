from flask import Blueprint, render_template, request, abort, current_app
from app.src.client import getQuote
import redis
import json

bp = Blueprint('stocks', __name__, url_prefix='/stocks')
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

def getStock(ticker):
    quote = getQuotes(ticker)
    ticker = quote['symbol']
    if not ticker:
        abort(400, 'Missing "ticker" parameter')
    return ticker, quote

@bp.route('/', methods=['GET','POST'])
def stocks():
    if request.method == 'GET':
        if redis_conn.get(ticker) == None:
            ticker2, stock = getStock(ticker)
            redis_conn.set(ticker, json.dumps(stock), ex=30)
            return render_template('stocks.html')
    elif request.method == 'POST':
        amount = request.form.get('amount')
        ticker = request.form.get('ticker')
        if not amount or not ticker:
            abort(400, 'Invalid amount or code')
        return render_template('purchase.html', ticker=ticker, amount=amount)

@app_route('/stock/<ticker>', methods=['GET'])
def specificStock(ticker):
    code = "code:" + ticker
    if redis_conn.get(ticker) == None:
        ticker2, stock = getStock(ticker)
        redis_conn.set(ticker, json.dumps(stock), ex=30)
    return render_template('stock.html', ticker=ticker)

def configure(app):
    app.register_blueprint(bp)

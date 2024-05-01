# #Import from the parent directory (app)
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from flask import Flask, Blueprint, request, jsonify, abort, make_response
# from app.db import db
# from app.src.client import getQuote
# import datetime
# import json
# import redis
# import sqlite3

# bp = Blueprint('stocks', __name__, url_prefix='/stock')
# redis_conn = redis.Redis(host='0.0.0.0', port=8000, password=os.environ.get('REDIS_PASSWORD'), db=0)

# def getStock(stock_symbol):
#     quote = getQuote(stock_symbol)
#     quote = json.dumps(quote)
#     return quote

# @bp.route('/stock')
# def hello():
#     return 'Hello, World!'

# @bp.route('/<string:stock_symbol>', methods=['GET'])
# def get_stock(stock_symbol):
#     if redis_conn.get(stock_symbol) is None:
#         quote = getStock(stock_symbol)
#         quote = json.dumps(quote)
#         redis_conn.setex(stock_symbol, 60, quote)
#     return jsonify(json.loads(redis_conn.get(stock_symbol)))

# @bp.route('/<string:stock_symbol>', methods=['POST'])
# def update_stock(stock_symbol):
#     amount = request.json.get('amount')

#     stock_symbol = stock_symbol.upper()

#     # Get the current date and time
#     now = datetime.datetime.now()
#     now = now.strftime("%Y-%m-%d %H:%M:%S")

#     if not amount:
#         abort(400, 'Invalid amount')
    
#     conn = db.get_db()
#     cursor = conn.cursor()
    
#     if db.check(conn, stock_symbol, now) == False:
#         db.insert(conn, stock_symbol, amount, now)

#     db.close()

#     return make_response(jsonify(f"{amount} stocks of {stock_symbol} purchased!"), 200)

# def configure(app):
#     app.register_blueprint(bp)
#     return app

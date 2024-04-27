from flask import Blueprint, render_template, request, abort
import json

bp = Blueprint('stocks', __name__, url_prefix='/stocks')
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

def getStock(stock):
    # TODO: Pegar o valor de stock proveniente da API Polygon
    stk = polygon 
    if not stk:
        abort(400, 'Missing "stk" parameter')


@bp.route('/', methods=['GET','POST'])
def stocks():
    if request.method == 'GET':
        # TODO: AINDA PRECISO CAPTURAR O CODIGO DA AÇÃO E PASSAR PARA O REDIS_CONN COMO STK
        # TODO: AINDA PRECISO PASSAR O CORPO DO JSON E PASSAR PARA O REDIS_CONN COMO VALOR A SER ARMAZENADO NO CACHE
        if redis_conn.get(code) == None:
            redis_conn.set(code, JSON, ex=30)
        return render_template('stocks.html')
    elif request.method == 'POST':
        amount = request.form.get('amount')
        code = request.form.get('code')
        if not amount or not code:
            abort(400, 'Invalid amount or code')
        return render_template('purchase.html')

# TODO: Connect to the purchase request
@app_route('/stock/<stk>', methods=['GET'])
def specificStock(stk):
    code = "code:" + stk
    if redis_conn.get(code) == None:
        stock = getStock(stk)
        redis_conn.set(code, json.dumps(stock), ex=30)
    return jsonify(json.loads(redis_con.get(code)))

def configure(app):
    app.register_blueprint(bp)

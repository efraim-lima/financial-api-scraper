from flask import Blueprint, render_template, request, abort
import redis

bp = Blueprint('purchase', __name__, url_prefix='/purchase')
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

@bp.route('/', methods=['GET','POST'])
def stocks():
    if request.method == 'GET':
        print(request.form)

        # AINDA PRECISO CAPTURAR O CODIGO DA AÇÃO E PASSAR PARA O REDIS_CONN COMO STK
        # AINDA PRECISO PASSAR O CORPO DO JSON E PASSAR PARA O REDIS_CONN COMO VALOR A SER ARMAZENADO NO CACHE
        if redis_conn.get(stk) == None:
            redis_conn.set(stk, JSON, ex=30)
        return render_template('stock.html')
    elif request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            abort(400, 'Invalid amount')
        return render_template('stock.html')
def configure(app):
    app.register_blueprint(bp)

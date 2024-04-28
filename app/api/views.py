from app import create_app
from flask import jsonify, render_template

def configure(app):
    @app.route('/')
    def api():
        return jsonify(data={'key':'value'})
    
    @app.route('/stocks')
    def stocks():
        return render_template(
            'index.html',
            title="Stocks"
            )
    
    @app.route('/stock/<sring:stock_symbol>')
    def purchase():
        return render_template(
            'index.html',
            title="Purchase"
            )


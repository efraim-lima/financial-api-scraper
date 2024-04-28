import views
import stocks
from flask import Flask
from app.api import stock

def create_app():
    app = Flask(__name__)
    views.configure(app)
    
    #extensão do arquivo
    stock.configure(app)
    
    app.register_blueprint(stock)
    
    @stock.after_request
    def wrap_response(response):
        response.headers.add('Content-Type', 'application/json')
        return response

    return app


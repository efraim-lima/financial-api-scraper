import views
import stocks
from flask import Flask

def create_app():
    app = Flask(__name__)
    views.configure(app)
    
    #extensão do arquivo
    stocks.configure(app)

    return app





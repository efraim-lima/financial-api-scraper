# Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import app.api.views
from flask import Flask
from app.api import stock
# from app.api import views
from app.api.stock import configure

def create_app():
    app = Flask(__name__)
    configure(app)
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run()
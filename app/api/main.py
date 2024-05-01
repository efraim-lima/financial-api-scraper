# Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import app.api.views
from flask import Flask
from app.api.views import configure as config

def create_app():
    app = Flask(__name__)
    config(app)
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)  
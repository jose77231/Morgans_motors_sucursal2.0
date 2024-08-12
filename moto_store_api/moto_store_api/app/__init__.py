# app/__init__.py

from flask import Flask
from flask_cors import CORS
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilitar CORS

    # Registrar rutas
    register_routes(app)

    return app

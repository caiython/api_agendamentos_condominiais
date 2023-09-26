from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from .routes.index import index_bp

app.register_blueprint(index_bp)
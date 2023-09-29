from flask import Blueprint

index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    return 'ta funcionando'

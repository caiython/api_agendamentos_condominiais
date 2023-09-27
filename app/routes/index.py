from flask import Blueprint, render_template

index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    return 'ta funcionando'

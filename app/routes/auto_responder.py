import json
from flask import Blueprint, request
from app import Condominio
import base64

auto_responder_bp = Blueprint('auto_responder_bp', __name__)

@auto_responder_bp.route('/auto_responder', methods=['POST'])
def auto_responder():
    
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json; charset=UTF-8",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Max-Age": "3600",
        "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    }

    data = request.get_json()
    request_headers = request.headers
    condominio = request_headers.get('Condominio')
    credenciais = f'{request_headers.get("Usuario")}:{request_headers.get("Senha")}'
    token = base64.b64encode((credenciais).encode('utf-8')).decode('utf-8')
    
    query_result = Condominio.query.filter_by(token=token).filter_by(nome=condominio.lower()).first()

    if ('query' in data and
        'appPackageName' in data and
        'messengerPackageName' in data and
        'sender' in data['query'] and
        'message' in data['query']
    ):

        sender = data['query']['sender']
        message = data['query']['message']

        response = {
            'replies': [
                {'message': f'{query_result.condominio_id}. {query_result.nome} - {query_result.endereco} '}
            ]
        }
        return json.dumps(response), 200, headers
    
    else:
        response = {
            "replies": [
                {"message": "Ocorreu um erro!"},
                {"message": "Os dados do JSON estão incompletos."},
                {"message": "A requisição foi enviada pelo AutoResponder?"}
            ]
        }

        return json.dumps(response), 400, headers

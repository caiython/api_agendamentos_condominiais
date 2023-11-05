from app import db
from .responses import Responses

def set_message(sender_message, cache_instance, user, condominio):

    if cache_instance.conteudo == '0':
        cache_instance.conteudo = '0_01'
        db.session.commit()
        return Responses.welcome(condominio.nome)
    
    elif cache_instance.conteudo == '0_01':
        expected_message = {
            '01': ['1', '01', 'reservas de espaços'],
            'f': ['f', 'finalizar', 'sair', 'cancelar', 'fechar']
        }
        if sender_message.lower() in expected_message['01']:
            cache_instance.conteudo = '0_01_01'
            db.session.commit()
            return Responses.space_reservation()
        elif sender_message.lower() in expected_message['f']:
            cache_instance.conteudo = '0'
            db.session.commit()
            return Responses.thank_you(condominio.nome)
        else:
            return Responses.invalid_code()

    elif cache_instance.conteudo == '0_01_01':
        #continuar desenvolvendo daqui
        pass
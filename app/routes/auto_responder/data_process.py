from app import db, Condominio, Usuario, CacheUsuario
from .set_message import set_message

class DataProcessing():

    def get_user(condominio, contato_usuario):
        return Usuario.query.join(Usuario.condominios).join(Condominio, Usuario.condominios).filter(Usuario.contato == contato_usuario,Condominio.condominio_id == condominio.condominio_id).first()
    
    def get_cache(condominio, usuario):
        cache_instance = CacheUsuario.query.filter_by(condominio=condominio, usuario=usuario, tipo='instance').first()
        if cache_instance is None:
            new_cache_instance = CacheUsuario(tipo='instance',conteudo='0',usuario=usuario,condominio=condominio)
            db.session.add(new_cache_instance)
            db.session.commit()
            return new_cache_instance
        else:
            return cache_instance

    def get_response(condominio, contato_usuario, sender_message):

        user = DataProcessing.get_user(condominio, contato_usuario)

        if user is None:
            return {'replies': [{'message': f'O seu contato não está cadastrado no banco do condomínio. Contate o administrador do condomínio para realizar o cadastro.'}]}

        cache_instance = DataProcessing.get_cache(condominio, user)

        message = set_message(sender_message, cache_instance, user, condominio)
        
        return {'replies': [{'message': f'{message}'}]}
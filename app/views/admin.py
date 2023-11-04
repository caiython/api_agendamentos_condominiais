from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField, StringField
from app import basic_auth, AuthException
from flask import redirect
import base64

class CondominioView(ModelView):

    column_list = ['condominio_id', 'nome', 'endereco', 'status', 'usuarios']
    column_labels = dict(condominio_id='ID')

    form_extra_fields = {
        'usuario_autenticacao': StringField('Usuario (Auth)'),
        'senha_autenticacao': PasswordField('Senha (Auth)')
    }
    form_columns = ['usuario_autenticacao', 'senha_autenticacao', 'nome', 'endereco', 'status', 'usuarios']
    
    def on_model_change(self, form, model, is_created):
        credenciais = f'{form.usuario_autenticacao.data}:{form.senha_autenticacao.data}'.encode('utf-8')
        model.token = base64.b64encode(credenciais).decode('utf-8')
    
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class UsuarioView(ModelView):
    column_list = ['usuario_id', 'nome_completo', 'contato', 'status', 'condominios']
    column_labels = dict(usuario_id='ID')
    form_columns = ['nome_completo', 'contato', 'status', 'condominios']

class CacheUsuarioView(ModelView):
    column_list = ['cache_id', 'tipo', 'conteudo', 'usuario', 'condominio']
    column_labels = dict(cache_id='ID')
    form_columns = ['tipo', 'conteudo', 'usuario', 'condominio']

class AreaView(ModelView):
    column_list = ['area_id', 'nome', 'descricao', 'capacidade', 'localizacao', 'condominio', 'horarios']
    column_labels = dict(area_id='ID')
    form_columns = ['nome', 'descricao', 'capacidade', 'localizacao', 'condominio', 'horarios']

class HorarioView(ModelView):
    column_list = ['horario_id', 'dia_da_semana', 'horario']
    column_labels = dict(horario_id='ID')
    form_columns = ['dia_da_semana', 'horario']

class AgendamentoView(ModelView):
    column_list = ['agendamento_id', 'data_hora', 'status', 'usuario', 'condominio', 'area']
    column_labels = dict(agendamento_id='ID')
    form_columns = ['data_hora', 'status', 'usuario', 'condominio', 'area']
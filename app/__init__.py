from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from .models import *
from .views.admin import *

admin = Admin(app)
admin.add_view(CondominioView(Condominio, db.session))
admin.add_view(UsuarioView(Usuario, db.session))
admin.add_view(CacheUsuarioView(CacheUsuario, db.session))
admin.add_view(AreaView(Area, db.session))
admin.add_view(HorarioView(Horario, db.session))
admin.add_view(AgendamentoView(Agendamento, db.session))

from .routes.index import index_bp
from .routes.auto_responder import auto_responder_bp

app.register_blueprint(index_bp)
app.register_blueprint(auto_responder_bp)
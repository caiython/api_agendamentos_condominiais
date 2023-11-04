from app import db

condominio_usuario = db.Table('CondominioUsuario',
    db.Column('condominio_usuario_id', db.Integer, primary_key=True),
    db.Column('funcao', db.Enum('morador', 'administrador', 'porteiro', 'visitante'), default='morador'),
    db.Column('condominio_id', db.Integer, db.ForeignKey('condominio.condominio_id')),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.usuario_id'))
)

class Condominio(db.Model):
    condominio_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    endereco =  db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum('ativo', 'inativo'), default='ativo', nullable=False)
    token = db.Column(db.String(100), nullable=False)
    usuarios = db.relationship('Usuario', secondary=condominio_usuario, lazy='subquery', backref=db.backref('condominios', lazy=True))

    def __repr__(self):
        return f'<{self.condominio_id}: {self.nome}>'

class Usuario(db.Model):
    __tablename__ = 'usuario'

    usuario_id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    contato = db.Column(db.String(13), unique=True, nullable=False)
    status = db.Column(db.Enum('ativo', 'inativo'), default='ativo', nullable=False)
    #instancia = db.Column(db.String(20), nullable=False, default='0')

    def __repr__(self):
        return f'<{self.usuario_id}: {self.nome_completo}>'

class CacheUsuario(db.Model):
    cache_id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    conteudo = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'))
    usuario = db.relationship('Usuario', backref=db.backref('cache', lazy='dynamic'))
    condominio_id = db.Column(db.Integer, db.ForeignKey('condominio.condominio_id'))
    condominio = db.relationship('Condominio', backref=db.backref('cache', lazy='dynamic'))

area_horario = db.Table('AreaHorario',
    db.Column('area_horario_id', db.Integer, primary_key=True),
    db.Column('area_id', db.Integer, db.ForeignKey('area.area_id')),
    db.Column('horario_id', db.Integer, db.ForeignKey('horario.horario_id'))
)

class Area(db.Model):
    area_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(300))
    capacidade = db.Column(db.Integer)
    localizacao = db.Column(db.String(30))
    condominio_id = db.Column(db.Integer, db.ForeignKey('condominio.condominio_id'))
    condominio = db.relationship('Condominio', backref=db.backref('area', lazy='dynamic'))
    horarios = db.relationship('Horario', secondary=area_horario, lazy='subquery', backref=db.backref('areas', lazy=True))

    def __repr__(self):
        return f'<{self.area_id}: {self.nome}>'

class Horario(db.Model):
    horario_id = db.Column(db.Integer, primary_key=True)
    dia_da_semana = db.Column(db.Enum('segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo'), nullable=False)
    horario = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<{self.horario_id}: {self.dia_da_semana}/{self.horario}>'

class Agendamento(db.Model):
    agendamento_id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('agendado', 'cancelado'), default='agendado', nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'))
    usuario = db.relationship('Usuario', backref=db.backref('agendamento', lazy='dynamic'))
    condominio_id = db.Column(db.Integer, db.ForeignKey('condominio.condominio_id'))
    condominio = db.relationship('Condominio', backref=db.backref('agendamento', lazy='dynamic'))
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'))
    area = db.relationship('Area', backref=db.backref('agendamento', lazy='dynamic'))


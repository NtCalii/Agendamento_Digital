from Database import db
from flask_login import UserMixin

class Usuarios(UserMixin, db.Model):
    __tablename__ = "Usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)

class Horarios(db.Model):
    __tablename__ = "Horarios"

    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(30), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("Usuarios.id"), nullable=False)
    usuario = db.relationship("Usuarios", backref=db.backref("horarios", lazy=True))

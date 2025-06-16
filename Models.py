from Database import db
from flask_login import UserMixin

class Usuarios(UserMixin, db.Model):
    __tablename__ = "Usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    
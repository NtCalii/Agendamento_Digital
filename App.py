from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from Database import db
from Models import Usuarios, Horarios
import hashlib
from datetime import date, time

app = Flask(__name__)
app.secret_key = "senha_secreta"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)
lm = LoginManager(app)
lm.login_view = "login"

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode("utf-8"))
    return hash_obj.hexdigest()

@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuarios).filter_by(id=id).first()
    return usuario

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("Login.html")
    elif request.method == "POST":
        nome = request.form["inputNome"]
        senha = request.form["inputSenha"]

        user = db.session.query(Usuarios).filter_by(nome=nome, senha=hash(senha)).first()
        if not user:
            return "Nome ou senha incorreto"
        
        login_user(user)
        return redirect(url_for("home"))

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("Cadastro.html")
    elif request.method == "POST":
        nome = request.form["inputNome"]
        email = request.form["inputEmail"]
        senha = request.form["inputSenha"]

        novo_usuario = Usuarios(nome=nome, email=email, senha=hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)

        return redirect(url_for("home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        return render_template("Home.html")
    elif request.method == "POST":
        nome_cliente = request.form["inputNomeCliente"]
        horario_str = request.form["inputHorario"]
        data_str = request.form["inputData"]
        usuario_id = current_user.id

        try:
            # Convertendo a data
            ano, mes, dia = map(int, data_str.split('-'))
            data_convertida = date(ano, mes, dia)

            # Convertendo o horário
            hora, minuto = map(int, horario_str.split(':'))
            horario_convertido = time(hora, minuto)

        except (ValueError, AttributeError):
            flash("Formato de data/horário inválido!", "error")
            return redirect(url_for("home"))

        novo_agendamento = Horarios(nome_cliente=nome_cliente, horario=horario_convertido, usuario_id=usuario_id, data=data_convertida)
        db.session.add(novo_agendamento)
        db.session.commit()

        return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

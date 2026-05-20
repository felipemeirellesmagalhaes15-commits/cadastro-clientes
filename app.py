from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from reportlab.pdfgen import canvas
from datetime import datetime
import os

app = Flask(__name__)

# CONFIG BANCO POSTGRESQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://cadastros_0uor_user:f5wUSv5tApZlp8QBhkb9J4hVeWX5jKGT@dpg-d86rkj7avr4c73edjl60-a.oregon-postgres.render.com/cadastros_0uor"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# TABELA CLIENTES
class Cliente(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    data = db.Column(db.String(50))
    razao_social = db.Column(db.String(200))
    cnpj = db.Column(db.String(50))
    ins_estadual = db.Column(db.String(50))
    data_nascimento = db.Column(db.String(50))
    cep = db.Column(db.String(50))
    endereco = db.Column(db.String(200))
    bairro = db.Column(db.String(100))
    telefone = db.Column(db.String(50))
    contato = db.Column(db.String(100))
    email = db.Column(db.String(150))
    ponto_referencia = db.Column(db.String(200))
    prazo_pagamento = db.Column(db.String(100))
    representante = db.Column(db.String(100))
    posicao = db.Column(db.String(100))
    destino_carro = db.Column(db.String(100))
    pedido = db.Column(db.String(200))


@app.route("/")
def inicio():
    return render_template("home.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        dados = request.form

        # SALVAR NO BANCO
        novo_cliente = Cliente(

            data=dados["data"],
            razao_social=dados["razao_social"],
            cnpj=dados["cnpj"],
            ins_estadual=dados["ins_estadual"],
            data_nascimento=dados["data_nascimento"],
            cep=dados["cep"],
            endereco=dados["endereco"],
            bairro=dados["bairro"],
            telefone=dados["telefone"],
            contato=dados["contato"],
            email=dados["email"],
            ponto_referencia=dados["ponto_referencia"],
            prazo_pagamento=dados["prazo_pagamento"],
            representante=dados["representante"],
            posicao=dados["posicao"],
            destino_carro=dados["destino_carro"],
            pedido=dados["pedido"]

        )

        db.session.add(novo_cliente)
        db.session.commit()

        # GERAR PDF
        representante = dados["representante"]
        razao_social = dados["razao_social"]

        pasta = f"pdfs/{representante}"

        os.makedirs(pasta, exist_ok=True)

        nome_pdf = f"{pasta}/{razao_social}.pdf"

        pdf = canvas.Canvas(nome_pdf)

        y = 800

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "Cadastro de Clientes - Fazenda das Antas")

        y -= 40

        for campo, valor in dados.items():

            pdf.setFont("Helvetica", 12)

            texto = f"{campo}: {valor}"

            pdf.drawString(50, y, texto)

            y -= 25

        pdf.save()

        return f"Cadastro salvo com sucesso para {razao_social}!"

    return render_template(
        "index.html",
        data_atual=datetime.now().strftime("%Y-%m-%d")
    )


# CRIAR TABELAS AUTOMATICAMENTE
with app.app_context():
    db.create_all()
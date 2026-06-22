from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from datetime import datetime
import os

app = Flask(__name__)

# NOVO BANCO POSTGRESQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://cadastros_t4v3_user:gHVzGQgrLZQ1CFNtVSQP4hKHvLvtPVi7@dpg-d8sjd2b6sc1c73cinr5g-a/cadastros_t4v3"

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

    # STATUS
    status = db.Column(db.String(50), default="PENDENTE")


@app.route("/")
def inicio():
    return render_template("home.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        dados = request.form

        novo_cliente = Cliente(

            data=dados.get("data"),
            razao_social=dados.get("razao_social"),
            cnpj=dados.get("cnpj"),
            ins_estadual=dados.get("ins_estadual"),
            data_nascimento=dados.get("data_nascimento"),
            cep=dados.get("cep"),
            endereco=dados.get("endereco"),
            bairro=dados.get("bairro"),
            telefone=dados.get("telefone"),
            contato=dados.get("contato"),
            email=dados.get("email"),
            ponto_referencia=dados.get("ponto_referencia"),
            prazo_pagamento=dados.get("prazo_pagamento"),
            representante=dados.get("representante"),
            posicao=dados.get("posicao"),
            destino_carro=dados.get("destino_carro"),
            pedido=dados.get("pedido")

        )

        db.session.add(novo_cliente)
        db.session.commit()

        return f"Cadastro salvo com sucesso para {dados.get('razao_social')}!"

    return render_template(
        "index.html",
        data_atual=datetime.now().strftime("%Y-%m-%d")
    )


@app.route("/relatorios")
def relatorios():

    clientes = Cliente.query.filter_by(status="PENDENTE").all()

    return render_template(
        "relatorios.html",
        clientes=clientes
    )


@app.route("/exportar_pdf/<int:id>")
def exportar_pdf(id):

    cliente = Cliente.query.get_or_404(id)

    nome_pdf = f"{cliente.razao_social}.pdf"

    pdf = canvas.Canvas(nome_pdf)

    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "CADASTRO DE CLIENTE")

    y -= 40

    dados = [

    f"DATA: {cliente.data.upper()}",
    f"RAZÃO SOCIAL: {cliente.razao_social.upper()}",
    f"CNPJ: {cliente.cnpj.upper()}",
    f"INSCRIÇÃO ESTADUAL: {cliente.ins_estadual.upper()}",
    f"DATA NASCIMENTO: {cliente.data_nascimento.upper()}",
    f"CEP: {cliente.cep.upper()}",
    f"ENDEREÇO: {cliente.endereco.upper()}",
    f"BAIRRO: {cliente.bairro.upper()}",
    f"TELEFONE: {cliente.telefone.upper()}",
    f"CONTATO: {cliente.contato.upper()}",

    # EMAIL MINÚSCULO
    f"EMAIL: {cliente.email.lower()}",

    f"PONTO REFERÊNCIA: {cliente.ponto_referencia.upper()}",
    f"PRAZO PAGAMENTO: {cliente.prazo_pagamento.upper()}",
    f"REPRESENTANTE: {cliente.representante.upper()}",
    f"POSIÇÃO: {cliente.posicao.upper()}",
    f"DESTINO CARRO: {cliente.destino_carro.upper()}",
    f"PEDIDO: {cliente.pedido.upper()}"

]

    for item in dados:

        pdf.setFont("Helvetica", 11)

        pdf.drawString(50, y, item)

        y -= 20

    pdf.save()

    # ALTERA STATUS
    cliente.status = "EXPORTADO"

    db.session.commit()

    return send_file(
        nome_pdf,
        as_attachment=True
    )


# CRIA TABELAS AUTOMATICAMENTE
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
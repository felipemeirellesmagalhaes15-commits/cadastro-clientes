from flask import Flask, render_template, request
from reportlab.pdfgen import canvas
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("home.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        dados = request.form

        representante = dados["representante"]
        razao_social = dados["razao_social"]

        # Criar pasta PDFs
        pasta = f"pdfs/{representante}"

        os.makedirs(pasta, exist_ok=True)

        # Nome PDF
        nome_pdf = f"{pasta}/{razao_social}.pdf"

        # Criar PDF
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

        return f"Cadastro salvo com sucesso! PDF gerado para {razao_social}"

    return render_template(
    "index.html",
    data_atual=datetime.now().strftime("%Y-%m-%d")
)


if __name__ == "__main__":
    app.run(debug=True)
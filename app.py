from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

# Criar a pasta static/ se não existir
if not os.path.exists("static"):
    os.makedirs("static")

# Página principal com formulário
@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h2>Preencher Relatório</h2>
            <form action="/gerar_pdf" method="post">
                Data: <input type="text" name="data"><br>
                Indicativo: <input type="text" name="indicativo"><br>
                Turno: <input type="text" name="turno"><br>
                Chefe de Viatura Nome: <input type="text" name="chefe_nome"><br>
                Chefe de Viatura Posto: <input type="text" name="chefe_posto"><br>
                Condutor Nome: <input type="text" name="condutor_nome"><br>
                Condutor Posto: <input type="text" name="condutor_posto"><br>
                Viatura Matrícula: <input type="text" name="viatura_matricula"><br>
                Viatura Modelo: <input type="text" name="viatura_modelo"><br>
                Ocorrências: <textarea name="ocorrencias"></textarea><br>
                <input type="submit" value="Gerar Relatório">
            </form>
        </body>
    </html>
    '''

# Geração do relatório em PDF
@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    # Capturar dados do formulário
    data = request.form['data']
    indicativo = request.form['indicativo']
    turno = request.form['turno']
    chefe_nome = request.form['chefe_nome']
    chefe_posto = request.form['chefe_posto']
    condutor_nome = request.form['condutor_nome']
    condutor_posto = request.form['condutor_posto']
    viatura_matricula = request.form['viatura_matricula']
    viatura_modelo = request.form['viatura_modelo']
    ocorrencias = request.form['ocorrencias']
    
    # Criar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, "RELATÓRIO DO CARRO PATRULHA", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, f"Data: {data}   Indicativo: {indicativo}    Turno: {turno}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, f"Chefe de Viatura: {chefe_posto} {chefe_nome}", ln=True)
    pdf.cell(200, 10, f"Condutor: {condutor_posto} {condutor_nome}", ln=True)
    pdf.cell(200, 10, f"Viatura: {viatura_matricula} - {viatura_modelo}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "RESUMO DAS OCORRÊNCIAS", ln=True, align='C')
    pdf.multi_cell(0, 10, ocorrencias)
    
    # Guardar o PDF
    pdf_filename = "relatorio_cp_funchal.pdf"
    pdf_path = os.path.join("static", pdf_filename)
    pdf.output(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


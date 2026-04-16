import os
from flask import Flask, render_template, request, send_file
import openai
from fpdf import FPDF

app = Flask(__name__)

# Utilise ta clé OpenAI ici
openai.api_key = "TA_CLE_ICI"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.form.get('user_input')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Recycle ceci : {user_input}"}]
        )
        resultat = response.choices[0].message.content
        return render_template('index.html', resultat_ia=resultat)
    except:
        return render_template('index.html', resultat_ia="Erreur de connexion API")

@app.route('/download-pdf', methods=['POST'])
def download():
    resultat_ia = request.form.get('resultat_ia', '')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=resultat_ia.encode('latin-1', 'replace').decode('latin-1'))
    path = "/tmp/rapport.pdf"
    pdf.output(path)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

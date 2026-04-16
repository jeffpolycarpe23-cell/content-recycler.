import os
from flask import Flask, render_template, request, send_file
import openai
from fpdf import FPDF

app = Flask(__name__)

# Configuration de la clé API OpenAI
openai.api_key = "TON_CODE_OPENAI_ICI"

@app.route('/')
def index():
    # Cette route affiche ton interface PolyContent
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.form.get('user_input')
    if not user_input:
        return "Veuillez entrer du texte."

    try:
        # Appel à OpenAI pour recycler le contenu
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en marketing digital."},
                {"role": "user", "content": f"Recycle ce contenu de manière experte : {user_input}"}
            ]
        )
        resultat = response.choices[0].message.content
        return render_template('index.html', resultat_ia=resultat)
    except Exception as e:
        return f"Erreur lors de l'analyse : {str(e)}"

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    # Récupère le texte généré pour le mettre dans le PDF
    resultat_ia = request.form.get('resultat_ia')
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Titre du document
    pdf.cell(200, 10, txt="Rapport d'Expert - PolyContent AI", ln=True, align='C')
    pdf.ln(10)
    
    # Contenu du rapport (nettoyage des caractères spéciaux pour FPDF)
    pdf.multi_cell(0, 10, txt=resultat_ia.encode('latin-1', 'replace').decode('latin-1'))
    
    path = "/tmp/rapport_expert.pdf"
    pdf.output(path)
    
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    # Configuration vitale pour Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

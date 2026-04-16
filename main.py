import os
import io
from flask import Flask, render_template, request, send_file
from openai import OpenAI  # Nouvelle syntaxe
from fpdf import FPDF

app = Flask(__name__)

# --- Configuration ---
client = OpenAI(api_key="TA_CLE_OPENAI_ICI") # Nouvelle manière d'appeler l'IA

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PolyContent AI - Rapport Expert', 0, 1, 'C')
        self.ln(10)

def generer_rapport_pdf(contenu):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Nettoyage des emojis pour éviter le crash du PDF
    texte_propre = contenu.encode('ascii', 'ignore').decode('ascii')
    texte_final = texte_propre.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=texte_final)
    return pdf.output(dest='S').encode('latin-1')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        prompt = request.form.get('user_input') # Vérifie que c'est bien 'user_input' dans ton HTML
        if prompt:
            try:
                # Nouvelle syntaxe OpenAI pour 2026
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un expert marketing. Utilise des emojis."},
                        {"role": "user", "content": f"Analyse ceci : {prompt}"}
                    ]
                )
                resultat_ia = response.choices[0].message.content
            except Exception as e:
                resultat_ia = f"Erreur de connexion : {str(e)}"
    
    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download():
    contenu = request.form.get('resultat_ia', '')
    pdf_data = generer_rapport_pdf(contenu)
    return send_file(io.BytesIO(pdf_data), mimetype='application/pdf', as_attachment=True, download_name='Rapport_Expert.pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

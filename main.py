import os
import io
from flask import Flask, render_template, request, send_file
from openai import OpenAI
from fpdf import FPDF

app = Flask(__name__)

# --- Configuration ---
# Utilise ta clé API OpenAI ici
client = OpenAI(api_key="TA_CLE_OPENAI_ICI")

class PDF(FPDF):
    def header(self):
        # En-tête élégant pour tes rapports PolyContent
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PolyContent AI - Rapport Strategique', 0, 1, 'C')
        self.ln(10)

def generer_rapport_pdf(contenu):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Nettoyage des emojis pour le PDF (obligatoire pour éviter les crashs)
    # Le PDF standard ne supporte pas les dessins d'emojis
    texte_sans_emoji = contenu.encode('ascii', 'ignore').decode('ascii')
    texte_propre = texte_sans_emoji.encode('latin-1', 'ignore').decode('latin-1')
    
    pdf.multi_cell(0, 10, txt=texte_propre)
    return pdf.output()

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        # Récupère l'idée du champ "user_input" de ton HTML
        prompt = request.form.get('user_input')
        
        if prompt:
            try:
                # Appel à l'IA avec la nouvelle syntaxe 2026
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un expert marketing. Utilise beaucoup d'emojis (🏠, 🚀, 💰) pour le rendu Web."},
                        {"role": "user", "content": f"Analyse et recycle ce contenu : {prompt}"}
                    ]
                )
                resultat_ia = response.choices[0].message.content
            except Exception as e:
                resultat_ia = f"Désolé, une petite erreur technique : {str(e)}"

    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download():
    # Récupère le texte généré pour le mettre dans le PDF
    contenu_final = request.form.get('resultat_ia', '')
    if not contenu_final:
        return "Erreur : Contenu introuvable", 400

    # Génération sécurisée du PDF
    pdf_bytes = generer_rapport_pdf(contenu_final)
    
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='Strategie_PolyContent.pdf'
    )

if __name__ == '__main__':
    # Configuration pour Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

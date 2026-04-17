import os
import io
from flask import Flask, render_template, request, send_file
from openai import OpenAI
from fpdf import FPDF

app = Flask(__name__)

# --- CONFIGURATION ---
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PolyContent AI - Rapport Strategique', 0, 1, 'C')
        self.ln(10)

def generer_rapport_pdf(contenu):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # ÉTAPE DE SÉCURITÉ : On retire les emojis qui font planter le PDF
    # On garde le texte et les accents, mais on ignore les symboles spéciaux
    texte_nettoyé = contenu.encode('ascii', 'ignore').decode('ascii')
    
    pdf.multi_cell(0, 10, txt=texte_nettoyé)
    return pdf.output(dest='S').encode('latin-1')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        prompt = request.form.get('user_input')
        service = request.form.get('service_type') 

        if prompt:
            try:
                if service == "immobilier":
                    system_msg = """Tu es un expert immobilier spécialisé sur Leboncoin et SeLoger. 
                    Analyse l'annonce et génère :
                    1. Une annonce optimisée pour Leboncoin/SeLoger.
                    2. Un script TikTok viral.
                    3. Un post LinkedIn et Instagram."""
                else:
                    system_msg = "Tu es un expert en freelance. Aide le client à rédiger un script de vente pour Upwork ou à résoudre un problème technique."

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                resultat_ia = f"Jeff, l'IA a analysé les meilleures réponses pour votre projet : \n\n" + response.choices[0].message.content
            
            except Exception as e:
                resultat_ia = f"Erreur technique : {str(e)}"

    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download():
    contenu_final = request.form.get('resultat_ia', '')
    if not contenu_final:
        return "Erreur : aucun contenu", 400
    try:
        pdf_bytes = generer_rapport_pdf(contenu_final)
        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name='Strategie_Jeff.pdf')
    except Exception:
        return "Erreur lors de la génération du PDF", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

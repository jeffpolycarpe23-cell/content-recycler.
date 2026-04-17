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
    # Correction PDF : On nettoie les caractères spéciaux pour éviter l'Internal Server Error
    texte_securise = contenu.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=texte_securise)
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
                    # Focus sur Leboncoin et SeLoger
                    system_msg = """Tu es un expert immobilier spécialisé sur Leboncoin et SeLoger. 
                    Analyse l'annonce et génère :
                    1. Une annonce optimisée pour Leboncoin/SeLoger (titre accrocheur, points forts).
                    2. Un script TikTok viral pour présenter ce bien.
                    3. Un post LinkedIn pour ton réseau pro.
                    4. Une légende Instagram avec emojis."""
                else:
                    system_msg = "Tu es un expert en freelance et prospection. Aide le client à rédiger un script de vente pour Upwork, à résoudre un problème technique ou à convaincre un client."

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                resultat_ia = f"Jeff, l'IA a analysé les meilleures réponses pour votre projet : \n\n" + response.choices[0].message.content
            
            except Exception as e:
                resultat_ia = f"Erreur de connexion : {str(e)}"

    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download():
    contenu_final = request.form.get('resultat_ia', '')
    if not contenu_final:
        return "Erreur : aucun contenu", 400
    pdf_bytes = generer_rapport_pdf(contenu_final)
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name='Strategie_Jeff.pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

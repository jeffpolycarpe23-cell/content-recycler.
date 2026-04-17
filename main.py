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
    texte_propre = contenu.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=texte_propre)
    return pdf.output(dest='S').encode('latin-1')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        prompt = request.form.get('user_input')
        # On récupère quel bouton a été cliqué
        service = request.form.get('service_type') 

        if prompt:
            try:
                # --- PERSONNALISATION SELON LE BOUTON ---
                if service == "immobilier":
                    system_msg = "Tu es un expert marketing immobilier. Pour chaque ville/sujet, génère 3 scripts : 1 TikTok viral, 1 post LinkedIn expert, et 1 légende Instagram avec emojis."
                else:
                    system_msg = "Tu es un expert en freelance et prospection. Aide le client à rédiger un script de vente, à résoudre un problème technique ou à convaincre un client sur Upwork."

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Phrase de réassurance au début
                resultat_ia = f"Jeff, l'IA a analysé les meilleures réponses pour votre projet : \n\n" + response.choices[0].message.content
            
            except Exception as e:
                resultat_ia = f"Note : Vérifiez votre clé API OpenAI. (Erreur: {str(e)})"

    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download():
    contenu_final = request.form.get('resultat_ia')
    if not contenu_final:
        return "Erreur : aucun contenu", 400
    pdf_bytes = generer_rapport_pdf(contenu_final)
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name='Strategie_Jeff.pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

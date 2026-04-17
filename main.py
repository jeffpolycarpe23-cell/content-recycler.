import os
import io
import re
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
    
    # NETTOYAGE RADICAL : On garde uniquement les lettres, chiffres et ponctuation de base
    # On enlève TOUT ce qui ressemble à un emoji ou un caractère spécial bizarre
    texte_propre = re.sub(r'[^\x00-\x7F]+', ' ', contenu)
    
    # On s'assure que le texte n'est pas vide
    if not texte_propre.strip():
        texte_propre = "Analyse PolyContent AI terminee."

    pdf.multi_cell(0, 10, txt=texte_propre)
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
                    system_msg = "Expert immobilier SeLoger/Leboncoin. Genere une annonce immo, un script TikTok et des posts reseaux sociaux."
                else:
                    system_msg = "Expert freelance. Aide a la redaction de scripts Upwork et resolution de problemes."

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ]
                )
                resultat_ia = f"Jeff, l'IA a analyse vos reponses : \n\n" + response.choices[0].message.content
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
    except Exception as e:
        # On affiche l'erreur réelle pour comprendre si ca bloque encore
        return f"Erreur PDF : {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

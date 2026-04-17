import os
import io
import re
from flask import Flask, render_template, request, send_file
from openai import OpenAI
from fpdf import FPDF

app = Flask(__name__)

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
    
    # Nettoyage strict pour éviter les erreurs PDF
    texte_propre = re.sub(r'[^\x00-\x7F]+', ' ', contenu)
    
    pdf.multi_cell(0, 10, txt=texte_propre)
    
    # LA CORRECTION : On retourne directement le flux binaire
    return pdf.output(dest='S')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        prompt = request.form.get('user_input')
        service = request.form.get('service_type') 
        if prompt:
            try:
                if service == "immobilier":
                    system_msg = "Expert immobilier SeLoger/Leboncoin. Génère une annonce, un script TikTok et des posts réseaux sociaux."
                else:
                    system_msg = "Expert freelance. Aide à la rédaction de scripts Upwork et résolution de problèmes."

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ]
                )
                resultat_ia = f"Jeff, l'IA a analyse vos reponses : \n\n" + response.choices[0].message.content
            except Exception as e:
                resultat_ia = f"Erreur : {str(e)}"
    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download():
    contenu_final = request.form.get('resultat_ia', '')
    if not contenu_final:
        return "Erreur : aucun contenu", 400
    try:
        # On récupère les données PDF déjà prêtes
        pdf_output = generer_rapport_pdf(contenu_final)
        return send_file(
            io.BytesIO(pdf_output), 
            mimetype='application/pdf', 
            as_attachment=True, 
            download_name='Strategie_Jeff.pdf'
        )
    except Exception as e:
        return f"Erreur PDF : {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

import os
import io
from flask import Flask, render_template, request, send_file
from openai import OpenAI
from fpdf import FPDF

app = Flask(__name__)

# --- CONFIGURATION ---
# REMPLACE BIEN TOUTE LA PHRASE ENTRE GUILLEMETS PAR TA VRAIE CLÉ (commençant par sk-...)
client = OpenAI(api_key="sk-PRO_VRAIE_CLE_ICI")

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PolyContent AI - Rapport Strategique', 0, 1, 'C')
        self.ln(10)

def generer_rapport_pdf(contenu):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    texte_sans_emoji = contenu.encode('ascii', 'ignore').decode('ascii')
    texte_final = texte_sans_emoji.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=texte_final)
    return pdf.output()

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        prompt = request.form.get('user_input')
        
        if prompt:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un expert marketing. Commence TOUJOURS tes réponses par : 'Jeff, l'IA a analysé les meilleures réponses à cette question ou proposition pour vous :' puis donne ton analyse avec des emojis."},
                        {"role": "user", "content": prompt}
                    ]
                )
                resultat_ia = response.choices[0].message.content
            except Exception as e:
                # On garde l'affichage propre même en cas d'erreur de clé
                resultat_ia = f"Note : Vérifiez votre clé API OpenAI dans le code. (Erreur: {str(e)})"

    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download():
    contenu_final = request.form.get('resultat_ia', '')
    if not contenu_final:
        return "Erreur", 400
    pdf_bytes = generer_rapport_pdf(contenu_final)
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name='Strategie_PolyContent.pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

import os
import io
from flask import Flask, render_template, request, send_file
from openai import OpenAI
from fpdf import FPDF

app = Flask(__name__)

# --- CONFIGURATION ---
# Mets ta clé complète entre les guillemets ci-dessous
client = OpenAI(api_key="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")

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PolyContent AI - Rapport Strategique', 0, 1, 'C')
        self.ln(10)

def generer_rapport_pdf(contenu):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Nettoyage pour éviter que le PDF ne plante avec les emojis
    texte_propre = contenu.encode('ascii', 'ignore').decode('ascii')
    texte_final = texte_propre.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=texte_final)
    return pdf.output()

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        prompt = request.form.get('user_input')
        
        if prompt:
            try:
                # C'est ici qu'on définit l'introduction personnalisée
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un expert marketing. Tu dois TOUJOURS commencer tes réponses par la phrase exacte : 'Jeff, l'IA a analysé les meilleures réponses à cette question ou proposition pour vous :' puis tu donnes ton analyse avec des emojis (🏠, 🚀, 💰)."},
                        {"role": "user", "content": prompt}
                    ]
                )
                resultat_ia = response.choices[0].message.content
            except Exception as e:
                resultat_ia = f"Note : Vérifiez votre clé API OpenAI. (Erreur: {str(e)})"

    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download():
    contenu_final = request.form.get('resultat_ia', '')
    if not contenu_final:
        return "Erreur", 400
    pdf_bytes = generer_rapport_pdf(contenu_final)
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name='Strategie_Jeff.pdf')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

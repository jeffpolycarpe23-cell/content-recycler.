import io
from flask import Flask, request, send_file, render_template
from fpdf import FPDF

app = Flask(__name__)

def creer_pdf_expert(contenu_ia):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Nettoyage rapide pour éviter les erreurs de caractères
    texte_propre = contenu_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, texte_propre)
    return pdf.output(dest='S')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        prompt = request.form.get('idee', '')
        # Simulation pour le test (On remettra l'IA après)
        resultat_ia = f"Analyse pour : {prompt}\n\nVotre projet a un fort potentiel."
    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    texte_ia = request.form.get('resultat_ia')
    if not texte_ia:
        return "Erreur : aucun contenu", 400
    
    pdf_bin = creer_pdf_expert(texte_ia)
    return send_file(
        io.BytesIO(pdf_bin),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='Rapport_Expert_PolyContent.pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

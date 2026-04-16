import io
import os
from flask import Flask, request, send_file, render_template
from fpdf import FPDF

app = Flask(__name__)

# --- CONFIGURATION DU RAPPORT PDF ---
def creer_pdf_expert(contenu_ia, nom_client="Client"):
    # On utilise 'P' pour Portrait, 'mm' pour millimètres et 'A4'
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # 1. Insertion du Logo
    try:
        # Assure-toi que logo.png est dans ton dossier sur ton MacBook
        pdf.image("logo.png", 10, 8, 30)
    except:
        pass 

    # 2. En-tête (Titre Bleu)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.set_xy(45, 15)
    pdf.set_text_color(36, 99, 235) # Ton bleu signature
    pdf.cell(0, 10, "POLYCONTENT AI - RAPPORT OFFICIEL", ln=True)
    
    # Ligne de séparation bleue
    pdf.set_draw_color(36, 99, 235)
    pdf.set_line_width(0.5)
    pdf.line(10, 40, 200, 40)
    
    pdf.ln(25) # Espace
    
    # 3. Corps du document
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, f"Analyse pour : {nom_client}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", size=11)
    # On utilise latin-1 pour la compatibilité, 'ignore' pour éviter les crashs sur les emojis
    texte_propre = contenu_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, texte_propre)
    
    # 4. Pied de page
    pdf.set_y(-20)
    pdf.set_font("Helvetica", 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "Produit généré par PolyContent AI - Nassau, Bahamas", align='C')
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- TES ROUTES FLASK ---

@app.route('/', methods=['GET', 'POST'])
def index():
    resultat_ia = None
    if request.method == 'POST':
        # Ton code de génération IA ici
        # simulation :
        prompt = request.form.get('idee', '')
        resultat_ia = f"Analyse stratégique terminée pour : {prompt}" 
    return render_template('index.html', resultat_ia=resultat_ia)

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    texte_ia = request.form.get('resultat_ia')
    if not texte_ia:
        return "Erreur", 400

    pdf_bin = creer_pdf_expert(texte_ia)
    
    return send_file(
        io.BytesIO(pdf_bin),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='Rapport_Expert_PolyContent.pdf'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

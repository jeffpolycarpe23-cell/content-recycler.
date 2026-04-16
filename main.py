import os
import openai
from flask import Flask, render_template_string, request

app = Flask(__name__)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

CODE_ACCES_VALIDE = "WORLD2026" 

HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PolyContent AI | Premium Hub</title>
    <style>
        :root { --primary: #2563eb; --dark: #0f172a; --gray: #1e293b; --text: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--dark); color: var(--text); margin: 0; padding: 0; }
        .navbar { background: var(--gray); padding: 1rem 2rem; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-weight: 800; font-size: 1.2rem; color: var(--primary); text-decoration: none; }
        .container { max-width: 600px; margin: 40px auto; padding: 20px; }
        .card { background: var(--gray); padding: 30px; border-radius: 24px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 5px; }
        p.subtitle { text-align: center; color: #94a3b8; margin-bottom: 25px; font-size: 0.9rem; }

        .mode-selector { display: flex; gap: 10px; margin-bottom: 20px; }
        .mode-btn { flex: 1; padding: 12px; border-radius: 12px; border: 2px solid #334155; background: #0f172a; color: #94a3b8; cursor: pointer; font-size: 0.85rem; font-weight: 600; transition: 0.3s; text-align: center; }
        
        /* Style quand un mode est sélectionné */
        input[type="radio"]:checked + label { border-color: var(--primary); color: white; background: rgba(37, 99, 235, 0.1); }

        input[type="text"], textarea { width: 100%; background: #0f172a; border: 2px solid #334155; border-radius: 15px; color: white; padding: 18px; font-size: 16px; margin-bottom: 15px; box-sizing: border-box; transition: 0.3s; }
        input:focus, textarea:focus { border-color: var(--primary); outline: none; }
        
        .code-field { text-align: center; font-weight: bold; color: var(--primary); border-style: dashed; letter-spacing: 2px; }
        
        #submit-btn { width: 100%; background: var(--primary); color: white; border: none; padding: 20px; border-radius: 15px; font-weight: 800; font-size: 1.1rem; cursor: pointer; transition: 0.3s; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3); }
        #submit-btn:disabled { background: #1e293b; cursor: wait; opacity: 0.8; }
        
        .result-box { margin-top: 30px; padding: 25px; background: #0f172a; border-radius: 15px; border-left: 5px solid var(--primary); line-height: 1.8; font-size: 15px; }
        .result-header { color: var(--primary); font-weight: bold; margin-bottom: 15px; display: block; font-size: 1.1rem; }
        
        .error { color: #ef4444; text-align: center; margin-bottom: 15px; background: rgba(239, 68, 68, 0.1); padding: 10px; border-radius: 10px; }
        .footer { text-align: center; margin-top: 40px; color: #475569; font-size: 0.8rem; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#" class="logo">POLYCONTENT AI</a>
        <div style="font-size: 0.7rem; border: 1px solid #475569; padding: 4px 12px; border-radius: 20px; color: #94a3b8;">PRO HUB</div>
    </nav>

    <div class="container">
        <div class="card">
            <h1>Propulsez votre Marketing 🚀</h1>
            <p class="subtitle">Analyse et création intelligente pour vos projets.</p>
            
            <form method="post" id="aiForm">
                <div class="mode-selector">
                    <input type="radio" name="mode" value="immo" id="immo" checked style="display:none">
                    <label for="immo" class="mode-btn">🏠 Immobilier</label>
                    
                    <input type="radio" name="mode" value="upwork" id="upwork" style="display:none">
                    <label for="upwork" class="mode-btn">💼 Freelance / Upwork</label>
                </div>

                <input type="text" name="access_code" id="access_code" class="code-field" placeholder="🔑 CODE ACCÈS" value="{{ last_code }}" required>
                <textarea name="content" id="content_area" placeholder="✨ Collez l'annonce ou l'idée ici..." required></textarea>
                
                <button type="submit" id="submit-btn">Générer la magie ✨</button>
            </form>

            {% if error %}<div class="error">{{ error }}</div>{% endif %}
            
            {% if result %}
            <div class="result-box">
                <span class="result-header">🎯 Votre stratégie sur mesure :</span>
                {{ result|safe }}
            </div>
            {% endif %}
        </div>
        <div class="footer">PolyContent AI &copy; 2026 - International Edition</div>
    </div>

    <script>
        const form = document.getElementById('aiForm');
        const btn = document.getElementById('submit-btn');

        form.onsubmit = function() {
            // Sauvegarde du code d'accès
            const codeInput = document.getElementById('access_code');
            localStorage.setItem('user_poly_code', codeInput.value);
            
            // Changement dynamique du bouton
            btn.disabled = true;
            btn.innerHTML = "⏳ L'IA analyse les meilleures stratégies...";
            btn.style.opacity = "0.7";
        };

        // Restauration automatique du code d'accès au chargement
        document.addEventListener("DOMContentLoaded", function() {
            const savedCode = localStorage.getItem('user_poly_code');
            if (savedCode) {
                document.getElementById('access_code').value = savedCode;
            }
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    user_code = ""
    if request.method == 'POST':
        user_code = request.form.get('access_code')
        user_text = request.form.get('content')
        mode = request.form.get('mode')
        
        if user_code == CODE_ACCES_VALIDE:
            try:
                # Définition des prompts avec exigence d'élégance et d'emojis
                if mode == "upwork":
                    prompt = f"Agis comme un expert freelance international. Analyse cette offre : '{user_text}'. Rédige une proposition de contrat irrésistible et un plan technique Python détaillé. Utilise une structure élégante, des titres clairs et beaucoup d'emojis pertinents."
                else:
                    prompt = f"Agis comme un expert marketing de luxe. Transforme ce texte : '{user_text}' en 1 Post LinkedIn captivant, 1 Thread Twitter percutant et 1 Script TikTok viral. Structure le contenu avec élégance, utilise des emojis et des sauts de ligne pour une lecture fluide."
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content.replace('\n', '<br>')
            except Exception as e:
                result = f"Erreur de connexion : {e}"
        else:
            error = "❌ Code incorrect. Accès refusé."
            
    return render_template_string(HTML, result=result, error=error, last_code=user_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

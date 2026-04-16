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
    <title>PolyContent AI | Business Hub</title>
    <style>
        :root { --primary: #2563eb; --dark: #0f172a; --gray: #1e293b; --text: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--dark); color: var(--text); margin: 0; padding: 0; min-height: 100vh; }
        .navbar { background: var(--gray); padding: 1rem 2rem; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-weight: 800; font-size: 1.2rem; color: var(--primary); text-decoration: none; letter-spacing: 1px; }
        .container { max-width: 650px; margin: 40px auto; padding: 20px; }
        .card { background: var(--gray); padding: 30px; border-radius: 28px; border: 1px solid #334155; box-shadow: 0 20px 50px rgba(0,0,0,0.6); }
        
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 8px; }
        p.subtitle { text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 0.95rem; }

        .mode-selector { display: flex; gap: 12px; margin-bottom: 25px; }
        .mode-btn { flex: 1; padding: 15px; border-radius: 15px; border: 2px solid #334155; background: #0f172a; color: #94a3b8; cursor: pointer; font-size: 0.85rem; font-weight: 700; transition: 0.3s; text-align: center; }
        
        input[type="radio"]:checked + label { border-color: var(--primary); color: white; background: rgba(37, 99, 235, 0.15); box-shadow: 0 0 15px rgba(37, 99, 235, 0.2); }

        input[type="text"], textarea { width: 100%; background: #0f172a; border: 2px solid #334155; border-radius: 18px; color: white; padding: 20px; font-size: 16px; margin-bottom: 15px; box-sizing: border-box; transition: 0.4s; }
        input:focus, textarea:focus { border-color: var(--primary); outline: none; background: #111b2e; }
        
        .code-field { text-align: center; font-weight: bold; color: var(--primary); border-style: dashed; letter-spacing: 3px; font-size: 1.2rem; }
        
        #submit-btn { width: 100%; background: var(--primary); color: white; border: none; padding: 22px; border-radius: 18px; font-weight: 800; font-size: 1.15rem; cursor: pointer; transition: 0.3s; box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4); margin-top: 10px; }
        #submit-btn:disabled { background: #1e293b; cursor: wait; transform: scale(0.98); }
        
        .result-box { margin-top: 35px; padding: 30px; background: #0b1120; border-radius: 20px; border: 1px solid #1e293b; line-height: 1.8; font-size: 15px; border-left: 6px solid var(--primary); }
        .result-header { color: var(--primary); font-weight: 800; margin-bottom: 20px; display: block; font-size: 1.2rem; text-transform: uppercase; }
        
        .error { color: #ef4444; text-align: center; margin-bottom: 15px; background: rgba(239, 68, 68, 0.1); padding: 12px; border-radius: 12px; font-weight: 600; }
        .footer { text-align: center; margin-top: 50px; color: #475569; font-size: 0.85rem; letter-spacing: 1px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#" class="logo">POLYCONTENT AI</a>
        <div style="font-size: 0.75rem; border: 1px solid #475569; padding: 5px 15px; border-radius: 25px; color: #94a3b8; font-weight: 600;">PRO EDITION</div>
    </nav>

    <div class="container">
        <div class="card">
            <h1>Générateur de Succès 🚀</h1>
            <p class="subtitle">Propulsez votre business immobilier ou freelance.</p>
            
            <form method="post" id="aiForm">
                <div class="mode-selector">
                    <input type="radio" name="mode" value="immo" id="immo" checked style="display:none">
                    <label for="immo" class="mode-btn">🏠 IMMOBILIER</label>
                    
                    <input type="radio" name="mode" value="upwork" id="upwork" style="display:none">
                    <label for="upwork" class="mode-btn">💼 FREELANCE PRO</label>
                </div>

                <input type="text" name="access_code" id="access_code" class="code-field" placeholder="🔑 CODE ACCÈS" value="{{ last_code }}" required>
                <textarea name="content" id="content_area" rows="6" placeholder="✨ Collez l'annonce Upwork ou l'idée de projet ici..." required></textarea>
                
                <button type="submit" id="submit-btn">LANCER L'ANALYSE ✨</button>
            </form>

            {% if error %}<div class="error">{{ error }}</div>{% endif %}
            
            {% if result %}
            <div class="result-box">
                <span class="result-header">🎯 Stratégie & Portfolio :</span>
                {{ result|safe }}
            </div>
            {% endif %}
        </div>
        <div class="footer">PolyContent AI &copy; 2026 - Designed by Jeff</div>
    </div>

    <script>
        const form = document.getElementById('aiForm');
        const btn = document.getElementById('submit-btn');

        form.onsubmit = function() {
            const codeInput = document.getElementById('access_code');
            localStorage.setItem('user_poly_code', codeInput.value);
            
            btn.disabled = true;
            btn.innerHTML = "⏳ L'IA analyse le marché international...";
            btn.style.opacity = "0.8";
        };

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
                if mode == "upwork":
                    prompt = (
                        f"Agis comme un expert freelance de classe mondiale. Analyse cette offre : '{user_text}'. "
                        "Fournis 3 éléments distincts et très élégants : "
                        "1. Une PROPOSITION DE CONTRAT irrésistible. "
                        "2. Un PLAN TECHNIQUE détaillé (Python/Automation). "
                        "3. Une FICHE PORTFOLIO prête à l'emploi qui résume ce projet pour tes futurs clients. "
                        "Utilise une structure de luxe, des titres clairs et beaucoup d'emojis."
                    )
                else:
                    prompt = (
                        f"Agis comme un expert marketing de luxe. Transforme ce texte : '{user_text}' "
                        "en : 1 Post LinkedIn captivant, 1 Thread Twitter percutant et 1 Script TikTok viral. "
                        "Utilise des emojis, des titres stylés et une mise en page aérée pour un rendu professionnel."
                    )
                
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

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
        .logo { font-weight: 800; font-size: 1.2rem; color: var(--primary); text-decoration: none; }
        .container { max-width: 650px; margin: 40px auto; padding: 20px; }
        .card { background: var(--gray); padding: 30px; border-radius: 28px; border: 1px solid #334155; box-shadow: 0 20px 50px rgba(0,0,0,0.6); }
        
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 8px; }
        .mode-selector { display: flex; gap: 12px; margin-bottom: 25px; margin-top: 20px; }
        .mode-btn { flex: 1; padding: 15px; border-radius: 15px; border: 2px solid #334155; background: #0f172a; color: #94a3b8; cursor: pointer; font-size: 0.85rem; font-weight: 700; transition: 0.3s; text-align: center; }
        
        input[type="radio"]:checked + label { border-color: var(--primary); color: white; background: rgba(37, 99, 235, 0.15); }

        input[type="text"], textarea { width: 100%; background: #0f172a; border: 2px solid #334155; border-radius: 18px; color: white; padding: 20px; font-size: 16px; margin-bottom: 15px; box-sizing: border-box; }
        .code-field { text-align: center; font-weight: bold; color: var(--primary); border-style: dashed; letter-spacing: 3px; }
        
        #submit-btn { width: 100%; background: var(--primary); color: white; border: none; padding: 22px; border-radius: 18px; font-weight: 800; font-size: 1.15rem; cursor: pointer; transition: 0.3s; box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4); }
        #submit-btn:disabled { background: #1e293b; cursor: wait; }
        
        .result-box { margin-top: 35px; padding: 30px; background: #0b1120; border-radius: 20px; border-left: 6px solid var(--primary); line-height: 1.8; color: #e2e8f0; }
        .result-header { color: var(--primary); font-weight: 800; margin-bottom: 20px; display: block; font-size: 1.2rem; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#" class="logo">POLYCONTENT AI</a>
        <div style="font-size: 0.75rem; border: 1px solid #475569; padding: 5px 15px; border-radius: 25px;">PRO HUB</div>
    </nav>

    <div class="container">
        <div class="card">
            <h1>Générateur de Succès 🚀</h1>
            <form method="post" id="aiForm">
                <div class="mode-selector">
                    <input type="radio" name="mode" value="immo" id="immo" checked style="display:none">
                    <label for="immo" class="mode-btn">🏠 IMMOBILIER</label>
                    <input type="radio" name="mode" value="upwork" id="upwork" style="display:none">
                    <label for="upwork" class="mode-btn">💼 FREELANCE PRO</label>
                </div>
                <input type="text" name="access_code" id="access_code" class="code-field" placeholder="🔑 CODE" value="{{ last_code }}" required>
                <textarea name="content" id="content_area" rows="5" placeholder="✨ Collez l'annonce Upwork ou l'idée ici..." required></textarea>
                <button type="submit" id="submit-btn">LANCER L'ANALYSE ✨</button>
            </form>

            {% if result %}
            <div class="result-box">
                <span class="result-header">🎯 VOTRE STRATÉGIE PERSONNALISÉE :</span>
                <div>{{ result|safe }}</div>
            </div>
            {% endif %}
        </div>
    </div>

    <script>
        document.getElementById('aiForm').onsubmit = function() {
            const btn = document.getElementById('submit-btn');
            localStorage.setItem('user_poly_code', document.getElementById('access_code').value);
            btn.disabled = true;
            btn.innerHTML = "⏳ L'IA analyse les meilleures stratégies...";
        };
        window.onload = function() {
            const savedCode = localStorage.getItem('user_poly_code');
            if (savedCode) document.getElementById('access_code').value = savedCode;
        };
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    last_code = ""
    if request.method == 'POST':
        last_code = request.form.get('access_code')
        content = request.form.get('content')
        mode = request.form.get('mode')
        
        if last_code == CODE_ACCES_VALIDE:
            try:
                # LOGIQUE DE RÉPONSE DIFFÉRENTE SELON LE MODE
                if mode == "upwork":
                    prompt = (
                        f"Tu es un expert en développement Python et automation. Analyse cette offre Upwork : '{content}'. "
                        "Ne recycle pas le texte. À la place, génère : "
                        "1. Une PROPOSITION DE CONTRAT convaincante pour décrocher la mission. "
                        "2. Une SOLUTION TECHNIQUE détaillée étape par étape. "
                        "3. Un résumé pour ton PORTFOLIO GitHub. "
                        "Utilise des emojis et un ton très pro."
                    )
                else:
                    prompt = (
                        f"Tu es un expert marketing immobilier de luxe. Transforme ce texte : '{content}' "
                        "en 1 Post LinkedIn, 1 Thread Twitter et 1 Script TikTok viral. "
                        "Utilise des emojis et un style élégant."
                    )

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content.replace('\n', '<br>')
            except Exception as e:
                result = f"Erreur : {e}"
        else:
            result = "❌ Code incorrect."
    return render_template_string(HTML, result=result, last_code=last_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

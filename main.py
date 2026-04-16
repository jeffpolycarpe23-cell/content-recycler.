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
    <title>PolyContent AI | Global Marketing</title>
    <style>
        :root { --primary: #2563eb; --dark: #0f172a; --gray: #1e293b; --text: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--dark); color: var(--text); margin: 0; padding: 0; }
        .navbar { background: var(--gray); padding: 1rem 2rem; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-weight: 800; font-size: 1.2rem; color: var(--primary); text-decoration: none; }
        .container { max-width: 600px; margin: 40px auto; padding: 20px; }
        .card { background: var(--gray); padding: 30px; border-radius: 24px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 5px; }
        p.subtitle { text-align: center; color: #94a3b8; margin-bottom: 25px; font-size: 0.9rem; }
        
        /* Design des champs */
        input, textarea { width: 100%; background: #0f172a; border: 2px solid #334155; border-radius: 15px; color: white; padding: 18px; font-size: 16px; margin-bottom: 15px; box-sizing: border-box; transition: 0.3s; }
        input:focus, textarea:focus { border-color: var(--primary); outline: none; background: #111b2e; }
        
        .code-field { text-align: center; font-weight: bold; letter-spacing: 2px; color: var(--primary); border-style: dashed; }
        
        button { width: 100%; background: var(--primary); color: white; border: none; padding: 20px; border-radius: 15px; font-weight: 800; font-size: 1.1rem; cursor: pointer; transition: 0.3s; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3); }
        button:hover { transform: translateY(-2px); background: #1d4ed8; }
        
        /* Zone de résultat avec style */
        .result-box { margin-top: 30px; padding: 25px; background: #0f172a; border-radius: 15px; border-left: 5px solid var(--primary); line-height: 1.8; font-size: 15px; position: relative; }
        .result-title { color: var(--primary); font-weight: bold; margin-bottom: 15px; display: block; font-size: 1.1rem; }
        
        .error { color: #ef4444; text-align: center; margin-bottom: 15px; background: rgba(239, 68, 68, 0.1); padding: 10px; border-radius: 10px; }
        .footer { text-align: center; margin-top: 40px; color: #475569; font-size: 0.8rem; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#" class="logo">POLYCONTENT AI</a>
        <div style="font-size: 0.7rem; border: 1px solid #475569; padding: 4px 12px; border-radius: 20px; color: #94a3b8;">GLOBAL ACCESS</div>
    </nav>

    <div class="container">
        <div class="card">
            <h1>Propulsez votre Marketing 🚀</h1>
            <p class="subtitle">Transformez vos idées en contenus viraux avec élégance.</p>
            
            <form method="post" id="aiForm">
                <input type="text" name="access_code" id="access_code" class="code-field" placeholder="🔑 CODE ACCÈS" value="{{ last_code }}" required>
                <textarea name="content" placeholder="✨ Collez votre texte ou description ici..." required></textarea>
                <button type="submit">Générer la magie ✨</button>
            </form>

            {% if error %}<div class="error">{{ error }}</div>{% endif %}
            
            {% if result %}
            <div class="result-box">
                <span class="result-title">🎯 Voici vos contenus recyclés :</span>
                {{ result|safe }}
            </div>
            {% endif %}
        </div>
        <div class="footer">PolyContent AI &copy; 2026 - International Edition</div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const inputCode = document.getElementById('access_code');
            const savedCode = localStorage.getItem('user_poly_code');
            if (savedCode && !inputCode.value) {
                inputCode.value = savedCode;
            }
            document.getElementById('aiForm').onsubmit = function() {
                localStorage.setItem('user_poly_code', inputCode.value);
            };
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
        if user_code == CODE_ACCES_VALIDE:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"Agis comme un expert marketing international. Transforme ce texte en : 1 Post LinkedIn captivant, 1 Thread Twitter percutant et 1 Script TikTok viral. Utilise BEAUCOUP d'emojis pertinents, des sauts de ligne clairs et un style très professionnel et visuel pour chaque format. Voici le texte : {user_text}"}]
                )
                result = response.choices[0].message.content.replace('\n', '<br>')
            except Exception as e:
                result = f"Erreur : {e}"
        else:
            error = "❌ Code incorrect."
    return render_template_string(HTML, result=result, error=error, last_code=user_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

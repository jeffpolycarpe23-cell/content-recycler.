import os
import openai
from flask import Flask, render_template_string, request

app = Flask(__name__)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Ton code secret global
CODE_ACCES_VALIDE = "WORLD2026" 

HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PolyContent AI | Global Access</title>
    <style>
        :root { --primary: #2563eb; --dark: #0f172a; --gray: #1e293b; --text: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--dark); color: var(--text); margin: 0; padding: 0; }
        .navbar { background: var(--gray); padding: 1rem 2rem; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-weight: 800; font-size: 1.2rem; color: var(--primary); text-decoration: none; }
        .container { max-width: 600px; margin: 40px auto; padding: 20px; }
        .card { background: var(--gray); padding: 30px; border-radius: 24px; border: 1px solid #334155; }
        input, textarea { width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 12px; color: white; padding: 15px; font-size: 16px; margin-bottom: 15px; box-sizing: border-box; }
        .code-field { border-color: var(--primary); text-align: center; font-weight: bold; }
        button { width: 100%; background: var(--primary); color: white; border: none; padding: 18px; border-radius: 12px; font-weight: 700; font-size: 1.1rem; cursor: pointer; transition: 0.3s; }
        .result-box { margin-top: 30px; padding: 20px; background: #0f172a; border-radius: 12px; border-left: 4px solid var(--primary); line-height: 1.6; }
        .error { color: #ef4444; text-align: center; margin-bottom: 15px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#" class="logo">POLYCONTENT AI</a>
        <div style="font-size: 0.7rem; border: 1px solid #475569; padding: 4px 10px; border-radius: 20px;">ACCÈS ILLIMITÉ</div>
    </nav>

    <div class="container">
        <div class="card">
            <form method="post" id="aiForm">
                <input type="text" name="access_code" id="access_code" class="code-field" placeholder="VOTRE CODE ACCÈS" required>
                <textarea name="content" id="content_area" placeholder="Collez votre texte ici..." required></textarea>
                <button type="submit">Générer les posts</button>
            </form>

            {% if error %}<div class="error">{{ error }}</div>{% endif %}
            {% if result %}<div class="result-box">{{ result|safe }}</div>{% endif %}
        </div>
    </div>

    <script>
        // Ce script s'exécute dans le téléphone du client
        document.addEventListener("DOMContentLoaded", function() {
            const inputCode = document.getElementById('access_code');
            
            // 1. On récupère le code s'il a déjà été sauvé
            const savedCode = localStorage.getItem('user_poly_code');
            if (savedCode) {
                inputCode.value = savedCode;
            }

            // 2. Juste avant d'envoyer le formulaire, on sauve le code
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
    if request.method == 'POST':
        user_code = request.form.get('access_code')
        user_text = request.form.get('content')
        if user_code == CODE_ACCES_VALIDE:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"Expert marketing international. Transforme ce texte en : 1 Post LinkedIn, 1 Thread Twitter et 1 Script TikTok : {user_text}"}]
                )
                result = response.choices[0].message.content.replace('\n', '<br>')
            except Exception as e:
                result = f"Erreur : {e}"
        else:
            error = "❌ Code invalide."
    return render_template_string(HTML, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

import os
import openai
from flask import Flask, render_template_string, request

app = Flask(__name__)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

CODE_ACCES_VALIDE = "WORLD2026" # Tu peux changer le code ici

HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PolyContent AI | Global Marketing Solution</title>
    <style>
        :root { --primary: #2563eb; --dark: #0f172a; --gray: #1e293b; --text: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--dark); color: var(--text); margin: 0; padding: 0; }
        .navbar { background: var(--gray); padding: 1rem 2rem; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-weight: 800; font-size: 1.2rem; color: var(--primary); text-decoration: none; }
        .container { max-width: 600px; margin: 40px auto; padding: 20px; }
        .card { background: var(--gray); padding: 30px; border-radius: 24px; border: 1px solid #334155; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 10px; }
        p.subtitle { text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 0.9rem; }
        input, textarea { width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 12px; color: white; padding: 15px; font-size: 16px; margin-bottom: 15px; box-sizing: border-box; }
        .code-field { border-color: var(--primary); text-align: center; font-weight: bold; }
        button { width: 100%; background: var(--primary); color: white; border: none; padding: 18px; border-radius: 12px; font-weight: 700; font-size: 1.1rem; cursor: pointer; transition: 0.3s; }
        button:hover { background: #1d4ed8; }
        .result-box { margin-top: 30px; padding: 20px; background: #0f172a; border-radius: 12px; border-left: 4px solid var(--primary); line-height: 1.6; }
        .error { color: #ef4444; text-align: center; margin-bottom: 15px; }
        .footer { text-align: center; margin-top: 40px; color: #475569; font-size: 0.8rem; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#" class="logo">POLYCONTENT AI</a>
        <div style="font-size: 0.7rem; border: 1px solid #475569; padding: 4px 10px; border-radius: 20px;">GLOBAL ACCESS</div>
    </nav>

    <div class="container">
        <div class="card">
            <h1>Propulsez votre Marketing</h1>
            <p class="subtitle">La solution IA pour transformer vos descriptions en contenus viraux, partout dans le monde.</p>
            
            <form method="post" id="mainForm">
                <input type="text" name="access_code" id="access_code" class="code-field" placeholder="MOT DE PASSE" required>
                <textarea name="content" placeholder="Collez votre annonce immobilière ou votre idée ici..." required></textarea>
                <button type="submit" onclick="saveCode()">Générer les posts</button>
            </form>

            {% if error %}<div class="error">{{ error }}</div>{% endif %}
            {% if result %}<div class="result-box">{{ result|safe }}</div>{% endif %}
        </div>
        <div class="footer">PolyContent AI &copy; 2026 - International Edition</div>
    </div>

    <script>
        window.onload = function() {
            const savedCode = localStorage.getItem('poly_code');
            if (savedCode) { document.getElementById('access_code').value = savedCode; }
        }
        function saveCode() {
            const code = document.getElementById('access_code').value;
            localStorage.setItem('poly_code', code);
        }
    </script>
</body>
</html>


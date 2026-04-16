import os
import openai
from flask import Flask, render_template_string, request

app = Flask(__name__)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PolyContent AI | Solution Marketing</title>
    <style>
        :root { --primary: #2563eb; --dark: #0f172a; --gray: #1e293b; --text: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--dark); color: var(--text); margin: 0; padding: 0; }
        .navbar { background: var(--gray); padding: 1rem 2rem; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-weight: 800; font-size: 1.5rem; color: var(--primary); text-decoration: none; }
        .container { max-width: 800px; margin: 40px auto; padding: 20px; }
        .hero { text-align: center; margin-bottom: 40px; }
        .hero h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .hero p { color: #94a3b8; font-size: 1.1rem; }
        .card { background: var(--gray); padding: 30px; border-radius: 24px; border: 1px solid #334155; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 150px; background: #0f172a; border: 1px solid #334155; border-radius: 12px; color: white; padding: 15px; font-size: 16px; margin-bottom: 20px; resize: none; }
        button { width: 100%; background: var(--primary); color: white; border: none; padding: 18px; border-radius: 12px; font-weight: 700; font-size: 1.1rem; cursor: pointer; transition: 0.3s; }
        button:hover { background: #1d4ed8; transform: translateY(-2px); }
        .result-box { margin-top: 30px; padding: 20px; background: #0f172a; border-radius: 12px; border-left: 4px solid var(--primary); line-height: 1.6; }
        .footer { text-align: center; margin-top: 60px; color: #64748b; font-size: 0.9rem; }
    </style>
</head>
<body>
    <nav class="navbar">
        <a href="#" class="logo">POLYCONTENT AI</a>
        <div style="font-size: 0.8rem; border: 1px solid #475569; padding: 4px 10px; border-radius: 20px;">PRO PLAN</div>
    </nav>

    <div class="container">
        <div class="hero">
            <h1>Recyclez votre contenu</h1>
            <p>L'IA premium pour les agents immobiliers et créateurs aux Bahamas.</p>
        </div>

        <div class="card">
            <form method="post">
                <textarea name="content" placeholder="Ex: Belle villa à Cable Beach avec vue mer..."></textarea>
                <button type="submit">Générer la stratégie multicanale</button>
            </form>

            {% if result %}
            <div class="result-box">
                {{ result|safe }}
            </div>
            {% endif %}
        </div>

        <div class="footer">
            &copy; 2026 PolyContent AI Nassau. Développé par Jeff.
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        user_text = request.form.get('content')
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Agis comme un expert marketing pro. Transforme ce texte en : 1 Post LinkedIn captivant, 1 Thread Twitter et 1 Script TikTok viral. Utilise des emojis pro et des sauts de ligne : {user_text}"}]
            )
            # On remplace les sauts de ligne par des balises <br> pour l'affichage HTML
            result = response.choices[0].message.content.replace('\n', '<br>')
        except Exception as e:
            result = f"Erreur de configuration : {e}"
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

import os
import openai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Lecture de ta clé secrète configurée sur Render
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Content Recycler Pro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; background: #f0f2f5; padding: 20px; }
        .card { max-width: 500px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 120px; border-radius: 12px; border: 1px solid #ddd; padding: 10px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; background: #007bff; color: white; border: none; padding: 15px; border-radius: 12px; margin-top: 15px; font-weight: bold; cursor: pointer; }
        .result { background: #f8f9fa; padding: 15px; border-radius: 12px; margin-top: 20px; white-space: pre-wrap; border-left: 5px solid #007bff; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="text-align:center">🚀 Content Recycler</h2>
        <form method="post">
            <textarea name="content" placeholder="Colle ton texte ou ton idée ici..."></textarea>
            <button type="submit">Générer les posts</button>
        </form>
        {% if result %}
            <div class="result"><strong>Tes contenus recyclés :</strong><br><br>{{ result }}</div>
        {% endif %}
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
            # Envoi du texte à l'IA
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Transforme ce texte en : 1 Post LinkedIn, 1 Thread Twitter et 1 script TikTok : {user_text}"}]
            )
            result = response.choices[0].message.content
        except Exception as e:
            result = f"Erreur de configuration : {e}"
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

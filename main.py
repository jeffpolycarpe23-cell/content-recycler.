from flask import Flask, render_template_string, request
import os
import openai

app = Flask(__name__)

# Interface HTML
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Recycleur Pro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f4f4f9; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 15px; }
        textarea { width: 100%; height: 100px; border-radius: 8px; border: 1px solid #ddd; }
        button { width: 100%; background: #007bff; color: white; border: none; padding: 12px; border-radius: 8px; margin-top: 10px; }
        .result { background: #e9ecef; padding: 15px; border-radius: 8px; margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 Content Recycler</h2>
        <form method="post">
            <textarea name="content" placeholder="Colle ton texte ici..."></textarea>
            <button type="submit">Générer les posts</button>
        </form>
        {% if result %}
            <div class="result">{{ result }}</div>
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
        # L'IA fonctionnera une fois qu'on aura mis la clé dans Render
        result = f"Texte reçu ! Ton projet avance Jeff. Prochaine étape : Render."
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

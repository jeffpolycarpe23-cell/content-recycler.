import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # On affiche juste ton interface pour tester la connexion
    return render_template('index.html')

if __name__ == '__main__':
    # On utilise le port 10000 qui est le standard chez Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

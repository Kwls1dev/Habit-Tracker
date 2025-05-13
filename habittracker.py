from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

ARQUIVO = "habitos.json"

# --- Funções auxiliares ---
def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return {}
    with open(ARQUIVO, 'r') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO, 'w') as f:
        json.dump(dados, f, indent=4)

# --- Rotas ---
@app.route('/')
def index():
    dados = carregar_dados()
    return render_template('index.html', habitos=dados)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome')
    dados = carregar_dados()
    if nome and nome not in dados:
        dados[nome] = []
        salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/marcar/<habito>', methods=['POST'])
def marcar(habito):
    hoje = datetime.now().strftime("%Y-%m-%d")
    dados = carregar_dados()
    if habito in dados and hoje not in dados[habito]:
        dados[habito].append(hoje)
        salvar_dados(dados)
    return redirect(url_for('index'))

@app.route('/progresso')
def progresso():
    dados = carregar_dados()
    progresso = {h: len(d) for h, d in dados.items()}
    return jsonify(progresso)

if __name__ == '__main__':
    app.run(debug=True)

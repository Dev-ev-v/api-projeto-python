from flask import Flask, request, jsonify

app = Flask(__name__)
tarefas = []

@app.route("/tarefas", methods=["GET"])
def listar():
    return jsonify({"tarefas": tarefas})

@app.route("/tarefas", methods=["POST"])
def adicionar():
    dados = request.get_json()

    if not dados or "tarefa" not in dados:
        return jsonify({"erro": "campo 'tarefa' obrigatório"}), 400

    tarefas.append(dados["tarefa"])
    return jsonify({"status": "adicionado", "tarefa": dados["tarefa"]}), 201

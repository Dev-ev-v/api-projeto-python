from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
tarefas = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tarefas", methods=["GET"])
def listar():
    return jsonify(tarefas)

@app.route("/tarefas", methods=["POST"])
def adicionar():
    dados = request.json
    tarefas.append(dados["tarefa"])
    return {"ok": True}

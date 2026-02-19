from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import jwt
import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY","devkey")

CORS(app, origins=["https://dev-ev-v.github.io"])

users = {}
tasks = {}

SECRET = os.environ["$jwt"]

def gerar_token(user):
    payload = {
        "user": user,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def auth_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        auth=request.headers.get("Authorization")

        if not auth:
            return {"success":False,"msg":"token ausente"},401

        try:
            token=auth.split()[1]
            data=jwt.decode(token,SECRET,algorithms=["HS256"])
            request.user=data["user"]
        except:
            return {"success":False,"msg":"token inválido"},401

        return f(*args,**kwargs)
    return wrapper

@app.route("/deploy", methods=["POST"])
def deploy():
    import os
    os.system("git pull origin main")
    return "Updated", 200

@app.post("/register")
def register():
    data = request.json
    user = data.get("user")
    password = data.get("password")

    if not user or not password:
        return {"success":False,"msg":"Campos obrigatórios"}

    if user in users:
        return {"success":False,"msg":"Usuário já existe"}

    users[user] = generate_password_hash(password)
    token = gerar_token(user)
    tasks[user] = []

    return {"success":True,"msg":"Conta criada","token":token}

@app.post("/login")
def login():
    data = request.json
    user = data.get("user")
    password = data.get("password")

    if user not in users:
        return {"success":False,"msg":"Credenciais inválidas"}

    if not check_password_hash(users[user],password):
        return {"success":False,"msg":"Credenciais inválidas"}

    token=gerar_token(user)
    return {"success":True,"msg":"Logado","token":token}

@app.get("/tasks")
@auth_required
def listar():
    user = request.user
    app.logger.debug("user:", user)
    return {"success":True,"tasks":tasks[user]}

@app.post("/tasks")
@auth_required
def add():
    user = request.user
    texto = request.json.get("task")
    app.logger.debug("texto da funcação add:", texto)
    if not texto:
        return {"success":False,"msg":"Vazio"}

    tasks.setdefault(user,[])
    tasks[user].append(texto)
    app.logger.debug("usuário e tasks do usuário:", user, tasks[user])
    return {"success":True,"msg":"Mensagem enviada com sucesso"}
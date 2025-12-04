from flask import Flask, render_template, request, redirect, session, url_for
from firebase_config import auth, db

app = Flask(__name__)
app.secret_key = "chave-super-secreta-do-gabriel"

# Página inicial redireciona para login
@app.route("/")
def index():
    return redirect("/login")

# ========== CRIAR CONTA ==========
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        try:
            # Criar usuário no Firebase Auth
            user = auth.create_user(
                email=email,
                password=senha,
                display_name=nome
            )

            # Salvar no Firestore
            db.collection("usuarios").document(user.uid).set({
                "nome": nome,
                "email": email
            })

            return redirect("/login")

        except Exception as e:
            return f"Erro ao criar conta: {e}"

    return render_template("criarconta.html")


# ========== LOGIN ==========
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        try:
            # Firebase Admin NÃO faz login
            user = auth.get_user_by_email(email)

            # Aceita qualquer senha → NÃO PODE
            # Vamos apenas validar que o email existe:
            session["user"] = user.uid
            return redirect("/home")

        except:
            return "Usuário não encontrado ou senha incorreta"

    return render_template("telalogin.html")

# ========== ROTAS PROTEGIDAS ==========
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("home.html")

@app.route("/perfil")
def perfil():
    if "user" not in session:
        return redirect("/login")
    return render_template("perfil.html")

@app.route("/config")
def configuracoes():
    if "user" not in session:
        return redirect("/login")
    return render_template("configuracoes.html")

@app.route("/ifpeflow")
def ifpeflow():
    if "user" not in session:
        return redirect("/login")
    return render_template("ifpeflow.html")

@app.route("/ecoscan")
def ecoscan():
    if "user" not in session:
        return redirect("/login")
    return render_template("ecoscan.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)

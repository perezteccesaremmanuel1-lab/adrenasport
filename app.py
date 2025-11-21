from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

client = MongoClient("mongodb+srv://perezteccesaremmanuel1_db_user:vBWeaxuovVUZGAQb@escuela.7uvtn09.mongodb.net/adrenasport")
db = client["adrenasport"]
usuarios = db["usuarios"]
productos = db["productos"]
carritos = db["carritos"]

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        contrasena = request.form["contrasena"].strip()

        user = usuarios.find_one({"usuario": usuario})
        if user:
            if user["contrasena"] == contrasena:
                session["usuario"] = usuario
                return redirect(url_for("inicio"))
            else:
                mensaje = "Contraseña incorrecta"
        else:
            mensaje = "Usuario no encontrado"

    return render_template("seseion.html", mensaje=mensaje)

# ---------------- REGISTRO ----------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        contrasena = request.form["contrasena"].strip()
        
        if usuarios.find_one({"usuario": usuario}):
            mensaje = "El usuario ya existe"
        else:
            usuarios.insert_one({"usuario": usuario, "contrasena": contrasena})
            return redirect(url_for("login"))
            
    return render_template("registro.html", mensaje=mensaje)

# ---------------- INICIO ----------------
@app.route("/inicio")
def inicio():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("INICIO.html")

# ---------------- SOCCER ----------------
@app.route("/soccer")
def soccer():
    if "usuario" not in session:
        return redirect(url_for("login"))
    productos_soccer = productos.find({"categoria": "soccer"})
    return render_template("soccer.html", productos=productos_soccer)

# ---------------- AMERICANO ----------------
@app.route("/americano")
def americano():
    if "usuario" not in session:
        return redirect(url_for("login"))
    productos_americano = productos.find({"categoria": "americano"})
    return render_template("americano.html", productos=productos_americano)

# ---------------- CARRITO ----------------
@app.route("/carrito")
def carrito():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("CARRITO.html")

# ---------------- GUARDAR CARRITO ----------------
@app.route("/guardar_carrito", methods=["POST"])
def guardar_carrito():
    if "usuario" not in session:
        return jsonify({"error": "Debes iniciar sesión"}), 401

    data = request.json
    productos_nuevos = data.get("productos", [])

    if not isinstance(productos_nuevos, list) or not productos_nuevos:
        return jsonify({"error": "Formato de productos inválido"}), 400

    usuario = session["usuario"]

    carrito_existente = carritos.find_one({"usuario": usuario})

    if carrito_existente:
        # Unimos listas sin anidar
        productos_actuales = carrito_existente.get("productos", [])
        productos_actualizados = productos_actuales + productos_nuevos
        carritos.update_one(
            {"usuario": usuario},
            {"$set": {"productos": productos_actualizados}}
        )
    else:
        carritos.insert_one({
            "usuario": usuario,
            "productos": productos_nuevos
        })

    return jsonify({"message": "🛒 Compra guardada correctamente en una sola lista"})

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)

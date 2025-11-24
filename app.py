from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave_super_secreta_por_defecto")

# Configuración de MongoDB
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

        # Validación básica
        if not usuario or not contrasena:
            mensaje = "Usuario y contraseña son requeridos"
        else:
            user = usuarios.find_one({"usuario": usuario})
            if user:
                if user["contrasena"] == contrasena:
                    session["usuario"] = usuario
                    return redirect(url_for("inicio"))
                else:
                    mensaje = "Contraseña incorrecta"
            else:
                mensaje = "Usuario no encontrado"

    return render_template("session.html", mensaje=mensaje)

# ---------------- REGISTRO ----------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        contrasena = request.form["contrasena"].strip()
        
        # Validación
        if not usuario or not contrasena:
            mensaje = "Usuario y contraseña son requeridos"
        elif len(usuario) < 3:
            mensaje = "El usuario debe tener al menos 3 caracteres"
        elif len(contrasena) < 4:
            mensaje = "La contraseña debe tener al menos 4 caracteres"
        else:
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
    return render_template("INICIO.html", usuario=session["usuario"])

# ---------------- SOCCER ----------------
@app.route("/soccer")
def soccer():
    if "usuario" not in session:
        return redirect(url_for("login"))
    productos_soccer = list(productos.find({"categoria": "soccer"}))
    return render_template("soccer.html", productos=productos_soccer, usuario=session["usuario"])

# ---------------- AMERICANO ----------------
@app.route("/americano")
def americano():
    if "usuario" not in session:
        return redirect(url_for("login"))
    productos_americano = list(productos.find({"categoria": "americano"}))
    return render_template("americano.html", productos=productos_americano, usuario=session["usuario"])

# ---------------- CARRITO ----------------
@app.route("/carrito")
def carrito():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    # Obtener el carrito del usuario
    usuario = session["usuario"]
    carrito_usuario = carritos.find_one({"usuario": usuario})
    productos_carrito = carrito_usuario.get("productos", []) if carrito_usuario else []
    
    return render_template("CARRITO.html", productos=productos_carrito, usuario=usuario)

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

# ---------------- VACIAR CARRITO ----------------
@app.route("/vaciar_carrito", methods=["POST"])
def vaciar_carrito():
    if "usuario" not in session:
        return jsonify({"error": "Debes iniciar sesión"}), 401
    
    usuario = session["usuario"]
    carritos.update_one(
        {"usuario": usuario},
        {"$set": {"productos": []}}
    )
    
    return jsonify({"message": "Carrito vaciado correctamente"})

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

# ---------------- MANEJO DE ERRORES ----------------
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Página no encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Error interno del servidor"), 500

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=False)  # Debug False para producción

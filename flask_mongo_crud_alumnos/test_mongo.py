# test_mongo.py
# 🔍 Este archivo sirve solo para probar la conexión a MongoDB y ver si existe tu usuario

from pymongo import MongoClient

try:
    # Conexión a MongoDB (asegúrate de que MongoDB esté corriendo)
    client = MongoClient("mongodb://localhost:27017/")

    # Seleccionar base de datos y colección
    db = client["adrenasport"]
    usuarios = db["usuarios"]

    # Mostrar todos los documentos en la colección
    print("✅ Conexión exitosa con MongoDB\n")
    print("📋 Usuarios en la colección:")
    encontrados = list(usuarios.find())

    if len(encontrados) == 0:
        print("⚠️ No hay usuarios en la colección. Inserta uno desde MongoDB Compass:")
        print("""
        {
          "usuario": "tecxito",
          "contrasena": "fanny"
        }
        """)
    else:
        for u in encontrados:
            print(u)

except Exception as e:
    print("❌ Error al conectar con MongoDB:")
    print(e)

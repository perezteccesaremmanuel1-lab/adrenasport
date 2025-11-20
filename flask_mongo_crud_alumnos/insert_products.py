from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["adrenasport"]
productos = db["productos"]

productos.delete_many({})

productos.insert_many([
    {"nombre": "Balón Adidas", "categoria": "soccer", "precio": 499, "imagen": "https://via.placeholder.com/200"},
    {"nombre": "Tacos Nike", "categoria": "soccer", "precio": 1199, "imagen": "https://via.placeholder.com/200"},
    {"nombre": "Casco Riddell", "categoria": "americano", "precio": 1499, "imagen": "https://via.placeholder.com/200"},
    {"nombre": "Jersey NFL", "categoria": "americano", "precio": 899, "imagen": "https://via.placeholder.com/200"}
])

print("✅ Productos insertados en MongoDB")

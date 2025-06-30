from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["viajes"]
usuarios = db["usuarios"]
viajes = db["viajes_deseados"]

usuarios_data = [
    {"nombre": "Lauren Mayberry", "cod": 10, "dinero_disponible": 500},
    {"nombre": "Hayley Williams", "cod": 5, "dinero_disponible": 600},
    {"nombre": "Dua Lipa", "cod": 20, "dinero_disponible": 10},
    {"nombre": "Carmen Electra", "cod": 15, "dinero_disponible": 50}
]

viajes_data = [
    {"usu": 10, "nom_lugar_inicio": "Cali", "nom_lugar_destino": "Villavicencio"},
    {"usu": 10, "nom_lugar_inicio": "Cali", "nom_lugar_destino": "Bogotá"},
    {"usu": 5, "nom_lugar_inicio": "Cali", "nom_lugar_destino": "Bogotá"},
    {"usu": 5, "nom_lugar_inicio": "Medellín", "nom_lugar_destino": "Bogotá"},
    {"usu": 20, "nom_lugar_inicio": "Villavicencio", "nom_lugar_destino": "Medellín"},
    {"usu": 15, "nom_lugar_inicio": "Villavicencio", "nom_lugar_destino": "Medellín"}
]

usuarios.delete_many({})
viajes.delete_many({})
usuarios.insert_many(usuarios_data)
viajes.insert_many(viajes_data)
print("MongoDB seed completo")

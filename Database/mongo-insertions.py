from pymongo import MongoClient

def insert_usuarios_y_viajes(usuarios_data, viajes_data, mongo_uri="mongodb://localhost:27017"):
    client = MongoClient(mongo_uri)
    db = client["viajes"]
    usuarios = db["usuarios"]
    viajes = db["viajes_deseados"]

    if usuarios_data:
        usuarios.insert_many(usuarios_data)
        print(f"{len(usuarios_data)} usuarios insertados.")
    if viajes_data:
        viajes.insert_many(viajes_data)
        print(f"{len(viajes_data)} viajes insertados.")

# Ejemplo de uso:
if __name__ == "__main__":
    usuarios = [
        {"nombre": "Ejemplo Usuario", "cod": 99, "dinero_disponible": 1000}
    ]
    viajes = [
        {"usu": 99, "nom_lugar_inicio": "Cali", "nom_lugar_destino": "Bogotá"}
    ]
    insert_usuarios_y_viajes(usuarios, viajes)
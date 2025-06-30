import os
from dotenv import load_dotenv
from punto1 import obtener_rutas_baratas

load_dotenv()

NEO4J_URI = os.getenv("DB_NEO4J_URL")
NEO4J_USER = os.getenv("DB_NEO4J_USER")
NEO4J_PASSWORD = os.getenv("DB_NEO4J_PASSWORD")
MONGO_URI = "mongodb://localhost:27017"

if __name__ == "__main__":
    obtener_rutas_baratas(
        cod_usuario=5,
        medio="avion",
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD,
        mongo_uri=MONGO_URI
    )
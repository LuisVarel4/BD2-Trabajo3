from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("DB_NEO4J_URL")
user = os.getenv("DB_NEO4J_USER")
password = os.getenv("DB_NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(user, password))

def insert_lugares(lugares):
    def _insert(tx):
        for lugar in lugares:
            tx.run("MERGE (:LUGAR {nombre: $nombre})", nombre=lugar)
    with driver.session() as session:
        session.execute_write(_insert)
    print(f"{len(lugares)} lugares insertados/actualizados.")

def insert_conexiones(conexiones):
    def _insert(tx):
        for origen, destino, dist, avion, bus in conexiones:
            tx.run(
                """
                MATCH (a:LUGAR {nombre: $origen}), (b:LUGAR {nombre: $destino})
                MERGE (a)-[:CONEXION {distancia: $dist, costo_avion: $avion, costo_bus: $bus}]->(b)
            """,
                origen=origen,
                destino=destino,
                dist=dist,
                avion=avion,
                bus=bus,
            )
    with driver.session() as session:
        session.execute_write(_insert)
    print(f"{len(conexiones)} conexiones insertadas/actualizadas.")

# Ejemplo de uso:
if __name__ == "__main__":
    lugares = ["Bogotá", "Medellín"]
    conexiones = [
        # Bogotá - Medellín
        ("Bogotá", "Medellín", 417, 52, 8),
        ("Medellín", "Bogotá", 417, 50, 7),
    ]
    insert_lugares(lugares)
    insert_conexiones(conexiones)
    driver.close()

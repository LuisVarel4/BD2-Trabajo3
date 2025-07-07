from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("DB_NEO4J_URL")
user = os.getenv("DB_NEO4J_USER")
password = os.getenv("DB_NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(user, password))

lugares = [
    "Cali", "Bogotá", "Medellín", "Villavicencio"
]

conexiones = [
    ("Cali", "Bogotá", 447, 70, 15),
    ("Bogotá", "Cali", 447, 65, 15),
    ("Cali", "Medellín", 435, 60, 10),
    ("Medellín", "Cali", 435, 55, 8),
    ("Bogotá", "Medellín", 417, 52, 8),
    ("Medellín", "Bogotá", 417, 50, 7),
    ("Bogotá", "Villavicencio", 128, 25, 5),
    ("Villavicencio", "Bogotá", 128, 25, 5),
]

def seed(tx):
    tx.run("MATCH (n) DETACH DELETE n")
    for lugar in lugares:
        tx.run("CREATE (:LUGAR {nombre: $nombre})", nombre=lugar)

    for origen, destino, dist, avion, bus in conexiones:
        tx.run(
            """
            MATCH (a:LUGAR {nombre: $origen}), (b:LUGAR {nombre: $destino})
            CREATE (a)-[:CONEXION {distancia: $dist, costo_avion: $avion, costo_bus: $bus}]->(b)
        """,
            origen=origen,
            destino=destino,
            dist=dist,
            avion=avion,
            bus=bus,
        )

with driver.session() as session:
    session.execute_write(seed)

print("Neo4j seed completo")

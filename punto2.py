from neo4j import GraphDatabase
import heapq
from pymongo import MongoClient

def dijkstra_con_camino(graph, start):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    queue = [(0, start)]
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)

        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, previous


def reconstruir_camino(previous, destino):
    path = []
    while destino:
        path.insert(0, destino)
        destino = previous[destino]
    return path


def construir_grafo_distancia(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    grafo = {}

    with driver.session() as session:
        query = """
        MATCH (a:LUGAR)-[r:CONEXION]->(b:LUGAR)
        RETURN a.nombre AS origen, b.nombre AS destino, r.distancia AS costo
        """

        result = session.run(query)
        for record in result:
            origen = record["origen"]
            destino = record["destino"]
            distancia = record["costo"]

            if origen not in grafo:
                grafo[origen] = {}
            grafo[origen][destino] = distancia

    return grafo


def obtener_viajes_deseados(cod_usuario, mongo_uri="mongodb://localhost:27017"):
    client = MongoClient(mongo_uri)
    db = client["viajes"]
    viajes = db["viajes_deseados"].find({"usu": cod_usuario})
    return list(viajes)


def obtener_rutas_mas_cortas(
    cod_usuario,
    neo4j_uri, neo4j_user, neo4j_password,
    mongo_uri="mongodb://localhost:27017"
):
    grafo = construir_grafo_distancia(neo4j_uri, neo4j_user, neo4j_password)
    viajes = obtener_viajes_deseados(cod_usuario, mongo_uri)

    for viaje in viajes:
        origen = viaje["nom_lugar_inicio"]
        destino = viaje["nom_lugar_destino"]

        if origen not in grafo:
            print(f"Origen {origen} no existe en el grafo")
            continue

        distances, previous = dijkstra_con_camino(grafo, origen)
        distancia_total = distances.get(destino)

        if distancia_total == float('inf'):
            print(f"No hay ruta de {origen} a {destino}")
        else:
            camino = reconstruir_camino(previous, destino)
            ruta_str = " -> ".join(camino)
            print(f"Ruta más corta por distancia de {origen} a {destino}: {ruta_str}, Distancia total: {distancia_total} km")

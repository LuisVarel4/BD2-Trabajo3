from pymongo import MongoClient
import heapq

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


def obtener_viajes_deseados(cod_usuario, mongo_uri="mongodb://localhost:27017"):
    client = MongoClient(mongo_uri)
    db = client["viajes"]
    viajes = db["viajes_deseados"].find({"usu": cod_usuario})
    return list(viajes)

from neo4j import GraphDatabase
from helpers import dijkstra_con_camino, reconstruir_camino, obtener_viajes_deseados

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


def obtener_rutas_mas_cortas(
    cod_usuario,
    neo4j_uri, neo4j_user, neo4j_password,
    mongo_uri="mongodb://localhost:27017"
):
    grafo = construir_grafo_distancia(neo4j_uri, neo4j_user, neo4j_password)
    viajes = obtener_viajes_deseados(cod_usuario, mongo_uri)

    print()
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

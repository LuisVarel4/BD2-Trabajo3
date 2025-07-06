from neo4j import GraphDatabase
from helpers import dijkstra_con_camino, reconstruir_camino, obtener_viajes_deseados

def construir_grafo(uri, user, password, modo):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    grafo = {}

    with driver.session() as session:
        query = """
        MATCH (a:LUGAR)-[r:CONEXION]->(b:LUGAR)
        RETURN a.nombre AS origen, b.nombre AS destino, r.%s AS costo
        """ % ("costo_bus" if modo == "bus" else "costo_avion")

        result = session.run(query)
        for record in result:
            origen = record["origen"]
            destino = record["destino"]
            costo = record["costo"]

            if origen not in grafo:
                grafo[origen] = {}
            grafo[origen][destino] = costo

    return grafo

def obtener_rutas_baratas(
    cod_usuario, medio, 
    neo4j_uri, neo4j_user, neo4j_password, 
    mongo_uri="mongodb://localhost:27017"
):
    grafo = construir_grafo(neo4j_uri, neo4j_user, neo4j_password, medio)
    viajes = obtener_viajes_deseados(cod_usuario, mongo_uri)

    print()
    for viaje in viajes:
        origen = viaje["nom_lugar_inicio"]
        destino = viaje["nom_lugar_destino"]

        if origen not in grafo:
            print(f"Origen {origen} no existe en el grafo")
            continue

        distances, previous = dijkstra_con_camino(grafo, origen)
        costo_total = distances.get(destino)

        if costo_total == float('inf'):
            print(f"No hay ruta de {origen} a {destino}")
        else:
            camino = reconstruir_camino(previous, destino)
            ruta_str = " -> ".join(camino)
            print(f"Ruta más barata de {origen} a {destino} ({medio}): {ruta_str}, Costo total: {costo_total}")

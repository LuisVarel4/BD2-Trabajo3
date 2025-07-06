from neo4j import GraphDatabase
from pymongo import MongoClient
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


def comparar_viajes_deseados(viajes_usuario_1, viajes_usuario_2):
    viajes_compartidos = []
    
    for viaje_usuario_1 in viajes_usuario_1:
        lugar_inicio = viaje_usuario_1["nom_lugar_inicio"]
        lugar_destino = viaje_usuario_1["nom_lugar_destino"]

        for viaje_usuario_2 in viajes_usuario_2:
            if (lugar_inicio == viaje_usuario_2["nom_lugar_inicio"] 
                and lugar_destino == viaje_usuario_2["nom_lugar_destino"]):
                viajes_compartidos.append(
                    [lugar_inicio, lugar_destino]
                )
        
    return viajes_compartidos


def obtener_dinero_total(cod_usuario_1, cod_usuario_2, mongo_uri="mongodb://localhost:27017"):
    client = MongoClient(mongo_uri)
    db = client["viajes"]
    dinero_usuario_1 = db["usuarios"].find({"cod": cod_usuario_1}, {"_id": 0, "dinero_disponible": 1})
    dinero_usuario_2 = db["usuarios"].find({"cod": cod_usuario_2}, {"_id": 0, "dinero_disponible": 1})

    dinero_usuario_1 = list(dinero_usuario_1)
    dinero_usuario_2 = list(dinero_usuario_2)
    
    return dinero_usuario_1[0]["dinero_disponible"] + dinero_usuario_2[0]["dinero_disponible"]


def obtener_viajes_en_comun(
    cod_usuario_1, cod_usuario_2, medio,
    neo4j_uri, neo4j_user, neo4j_password, 
    mongo_uri="mongodb://localhost:27017"
):
    grafo = construir_grafo(neo4j_uri, neo4j_user, neo4j_password, medio)

    viajes_usuario_1 = obtener_viajes_deseados(cod_usuario_1, mongo_uri)
    viajes_usuario_2 = obtener_viajes_deseados(cod_usuario_2, mongo_uri)

    viajes_compartidos = comparar_viajes_deseados(viajes_usuario_1, viajes_usuario_2)

    print()
    if viajes_compartidos:
        dinero_usuarios = obtener_dinero_total(cod_usuario_1, cod_usuario_2, mongo_uri)
        
        for viaje in viajes_compartidos:
            origen = viaje[0]
            destino = viaje[1]

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
                print(f"Ruta más barata de {origen} a {destino} ({medio}): {ruta_str}, Costo: {costo_total}")
                print(f"Costo total para dos personas: {costo_total*2}")

                print(f"Los usuarios tienen dinero disponible total de: {dinero_usuarios} y", end=" ")
                print("les alcanza para realizar el viaje") if costo_total*2 <= dinero_usuarios else print("no les alcanza para realizar el viaje")

    else:
        print("Los usuarios no tienen viajes en común")

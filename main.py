import os
from dotenv import load_dotenv
from punto1 import obtener_rutas_baratas
from punto2 import obtener_rutas_mas_cortas
from punto3 import obtener_viajes_en_comun

load_dotenv()

NEO4J_URI = os.getenv("DB_NEO4J_URL")
NEO4J_USER = os.getenv("DB_NEO4J_USER")
NEO4J_PASSWORD = os.getenv("DB_NEO4J_PASSWORD")
MONGO_URI = "mongodb://localhost:27017"

def obtener_cod_usuario(mensaje):
    while True:
        try:
            cod_usuario = int(input(mensaje))
            return cod_usuario
        except ValueError:
            print("Por favor, ingresa un número válido")


def obtener_medio_transporte(mensaje):
    while True:
        medio = input(mensaje).strip().lower()
        if medio in ["bus", "avion"]:
            return medio
        else:
            print("Los medios de transporte permitidos son 'bus' o 'avion', por favor intenta de nuevo")


def obtener_opcion():
    while True:
        try:
            opcion = int(input("Selecciona una opción (1-4): "))
            if opcion in [1, 2, 3, 4]:
                return opcion
            else:
                print("Por favor selecciona una de las opciones válidas del Menú (1-4)")
        except ValueError:
            print("Por favor ingresa un número válido")


if __name__ == "__main__":

    print("Bases de Datos 2: Trabajo 3\n")
    print("===========================\n")
    print("Menú Principal")
    print("1. Rutas Baratas")
    print("2. Rutas Más Cortas")
    print("3. Viajes En Común")
    print("4. Salir")
    print("\n===========================\n")

    while True:
        opcion = obtener_opcion()

        if opcion == 1:
            print("\nPunto 1: Rutas Baratas")

            cod_usuario = obtener_cod_usuario("Por favor ingresa el código del usuario: ")
            medio_transporte = obtener_medio_transporte("Por favor ingresa el medio de transporte preferido por el usuario: ")
            
            obtener_rutas_baratas(
                cod_usuario=cod_usuario,
                medio=medio_transporte,
                neo4j_uri=NEO4J_URI,
                neo4j_user=NEO4J_USER,
                neo4j_password=NEO4J_PASSWORD,
                mongo_uri=MONGO_URI
            )
            print()
        
        elif opcion == 2:
            print("\nPunto 2: Rutas Más Cortas")

            cod_usuario = obtener_cod_usuario("Por favor ingresa el código del usuario: ")
            
            obtener_rutas_mas_cortas(
                cod_usuario=cod_usuario,
                neo4j_uri=NEO4J_URI,
                neo4j_user=NEO4J_USER,
                neo4j_password=NEO4J_PASSWORD,
                mongo_uri=MONGO_URI,
            )
            print()

        elif opcion == 3:
            print("\nPunto 3: Viajes En Común")

            cod_usuario_1 = obtener_cod_usuario("Por favor ingresa el código del primer usuario: ")
            cod_usuario_2 = obtener_cod_usuario("Por favor ingresa el código del segundo usuario: ")
            medio_transporte = obtener_medio_transporte("Por favor ingresa el medio de transporte preferido por los usuarios: ")
            
            obtener_viajes_en_comun(
                cod_usuario_1=cod_usuario_1,
                cod_usuario_2=cod_usuario_2,
                medio=medio_transporte,
                neo4j_uri=NEO4J_URI,
                neo4j_user=NEO4J_USER,
                neo4j_password=NEO4J_PASSWORD,
                mongo_uri=MONGO_URI,
            )
            print()

        else:
            print("\n¡Gracias por tu visita!")
            break

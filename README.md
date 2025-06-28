# Trabajo 3 - Bases de Datos 2

## Requisitos

- [MongoDB Community Edition](https://www.mongodb.com/try/download/community)
- [Neo4j Community Edition](https://neo4j.com/download/)
- Python 3.x

## Instalación

1. **Clona este repositorio**

2. **Instala las dependencias de Python**

   ```sh
   pip install pymongo neo4j python-dotenv
   ```

3. **Configura las variables de entorno**

   - Crea un archivo `.env` en la raíz del proyecto.
   - Usa el archivo `.env.example` como referencia y completa tus credenciales y puertos según tu configuración.

4. **Carga los datos de ejemplo**

   Ejecuta los siguientes scripts para poblar las bases de datos:

   ```sh
   python mongo-seeder.py
   python neo4j-seeder.py
   ```

5. **Desarrolla tu solución**

   Trabaja en el archivo principal `main.py` para resolver el punto solicitado.

---

**¡Listo! Ahora puedes comenzar a trabajar en tu solución.**

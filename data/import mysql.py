import mysql.connector

# Establecer conexión
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tienda_vj"
)

if conn.is_connected():
    print("Conectado a MySQL")
else:
    print("No se pudo conectar")
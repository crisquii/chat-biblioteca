import mysql.connector

# Establecer conexión
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tienda"
)

if conn.is_connected():
    print("Conectado a MySQL")
else:
    print("No se pudo conectar")

cursor = conn.cursor()

# Insertar datos
query = "INSERT INTO productos (nombre, precio) VALUES (%s, %s)"
valores = ("camiseta", 20)
cursor.execute(query, valores)
conn.commit()

print(cursor.rowcount, "registro(s) insertado(s)")


# Consultar datos
cursor.execute("SELECT * FROM productos")
resultados = cursor.fetchall()

for fila in resultados:
    print(fila)

    # Actualizar datos
query = "UPDATE productos SET precio = %s WHERE nombre = %s"
valores = (31, "pantalones")
cursor.execute(query, valores)
conn.commit()

print(cursor.rowcount, "registro(s) actualizado(s)")
                
                
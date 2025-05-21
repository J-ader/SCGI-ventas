from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Conexión a la base de datos
app.config["MYSQL_HOST"] = "localhost"  # Host de la base de datos
app.config["MYSQL_USER"] = "root"  # Usuario de la base de datos
app.config["MYSQL_PASSWORD"] = "2569"  # Contraseña de la base de datos
app.config["MYSQL_DB"] = "GestionMed"  # Nombre de la base de datos

mysql = MySQL(app)  # Inicializa la extensión MySQL con la app Flask


#prueba para saber si la base de datos se conecta correctamente
try:
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        print("✅ Conexión exitosa a la base de datos")
except Exception as e:
    print(f"❌ Error al conectar a la base de datos: {e}")

  

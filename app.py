from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Conexión a la base de datos
app.config["MYSQL_HOST"] = "localhost"  # Host de la base de datos
app.config["MYSQL_USER"] = "root"  # Usuario de la base de datos
app.config["MYSQL_PASSWORD"] = "2569"  # Contraseña de la base de datos
app.config["MYSQL_DB"] = "gestion_med"  # Nombre de la base de datos

mysql = MySQL(app)  # Inicializa la extensión MySQL con la app Flask


#prueba para saber si la base de datos se conecta correctamente
""" try:
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        print("✅ Conexión exitosa a la base de datos")
except Exception as e:
    print(f"❌ Error al conectar a la base de datos: {e}")
 """
  

# Registro de usuario
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]  # Nombre del usuario
        apellido = request.form["apellido"]  # Apellido del usuario
        telefono = request.form["telefono"]  # Teléfono del usuario
        email = request.form["email"]  # Email del usuario
        fecha_nacimiento = request.form.get("fecha_nacimiento", "2000-01-01")  # Fecha de nacimiento
        contraseña = generate_password_hash(request.form["password"])  # Contraseña hasheada

        cur = mysql.connection.cursor()  # Cursor para ejecutar consultas
        cur.execute("""
            INSERT INTO usuarios (nombre, apellido, telefono, email, fecha_nacimiento, contraseña)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, telefono, email, fecha_nacimiento, contraseña))
        mysql.connection.commit()  # Guarda los cambios en la base de datos
        cur.close()  # Cierra el cursor

        flash("Cuenta creada exitosamente. Ahora puedes iniciar sesión.")  # Mensaje de éxito
        return redirect(url_for("login"))  # Redirige al login

    return render_template("registro.html")  # Muestra el formulario de registro

# Inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]  # Email ingresado
        password = request.form["password"]  # Contraseña ingresada

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        row = cur.fetchone()  # Obtiene el usuario si existe
        column_names = [desc[0] for desc in cur.description]  # Nombres de columnas
        usuario = dict(zip(column_names, row)) if row else None  # Diccionario usuario
        cur.close()

        # Verifica si el usuario existe y la contraseña es correcta
        if usuario and check_password_hash(usuario["contraseña"], password):
            session["username"] = usuario.get("nombre", usuario.get("username", ""))  # Guarda nombre en sesión
            session["nombre"] = usuario["nombre"]  # Guarda nombre en sesión para dashboard
            return redirect(url_for("dashboard"))  # Redirige al dashboard
        else:
            flash("Credenciales inválidas")  # Mensaje de error

    return render_template("login.html")  # Muestra el formulario de login



# Ejecuta la aplicación en modo debug
if __name__ == "__main__":
    app.run(debug=True)

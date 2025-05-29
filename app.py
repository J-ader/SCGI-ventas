from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret_key"

# Conexión a la base de datos
app.config["MYSQL_HOST"] = "localhost"  # Host de la base de datos
app.config["MYSQL_USER"] = "root"  # Usuario de la base de datos
app.config["MYSQL_PASSWORD"] = "2569"  # Contraseña de la base de datos
app.config["MYSQL_DB"] = "gestion_med"  # Nombre de la base de datos

mysql = MySQL(app)  # Inicializa la extensión MySQL con la app Flask


# prueba para saber si la base de datos se conecta correctamente
#
try:
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        print("✅ Conexión exitosa a la base de datos")
except Exception as e:
    print(f"❌ Error al conectar a la base de datos: {e}")


@app.route("/")
def home():
    return render_template("index.html")

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
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        row = cur.fetchone()
        column_names = [desc[0] for desc in cur.description]
        usuario = dict(zip(column_names, row)) if row else None
        cur.close()

        if usuario and check_password_hash(usuario["contraseña"], password):
            session["nombre"] = usuario["nombre"]
            session["email"] = usuario["email"]
            session["rol"] = usuario["rol"]

            flash("Inicio de sesión exitoso", "success")

            # Redirección según el rol
            if usuario["rol"] == "admin":
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("productos"))

        flash("Credenciales inválidas", "error")
    return render_template("login.html")

def process_email(email):
    """Corrige el error anterior y permite procesar el email correctamente."""
    print(f"Procesando email: {email}")


# Decorador para verificar si el usuario ha iniciado sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "nombre" not in session:
            flash("Debes iniciar sesión para acceder.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/productos")
def productos():
   
    return render_template("productos.html")

# Ruta para la cuenta del usuario, muestra sus datos
@app.route("/account")
@login_required
def account():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = %s", (session['email'],))
    row = cur.fetchone()
    column_names = [desc[0] for desc in cur.description]
    usuario = dict(zip(column_names, row)) if row else None
    cur.close()
    return render_template("account.html", usuario=usuario)


# Panel principal, muestra todos los usuarios si hay sesión activa

@app.route("/dashboard")
@login_required
def dashboard():
    if session.get("rol") != "admin":
        flash("Acceso denegado: solo administradores", "error")
        return redirect(url_for("productos"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    column_names = [desc[0] for desc in cur.description]
    usuarios = [dict(zip(column_names, row)) for row in cur.fetchall()]
    cur.close()
    #return render_template("productos.html", usuarios=usuarios)
    return render_template("dashboard.html", usuarios=usuarios)  # Muestra el dashboard con usuarios




# Eliminar usuario por ID
@app.route("/delete/<int:id>")
@login_required
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))  # Elimina usuario por ID
    flash("Eliminado", "danger") # Mensaje de eliminación bbp
    mysql.connection.commit()
    cur.close()

    flash("Usuario eliminado correctamente","success")  # Mensaje de éxito
    return redirect(url_for("dashboard"))  # Redirige al dashboard

# Editar usuario por ID
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    cur = mysql.connection.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]  # Nuevo nombre
        apellido = request.form["apellido"]  # Nuevo apellido
        telefono = request.form["telefono"]  # Nuevo teléfono
        email = request.form["email"]  # Nuevo email
        fecha_nacimiento = request.form["fecha_nacimiento"]  # Nueva fecha de nacimiento

        cur.execute("""
            UPDATE usuarios
            SET nombre = %s, apellido = %s, telefono = %s, email = %s, fecha_nacimiento = %s
            WHERE id = %s
        """, (nombre, apellido, telefono, email, fecha_nacimiento, id))  # Actualiza datos

        mysql.connection.commit()
        cur.close()

        flash("Usuario actualizado correctamente","success")  # Mensaje de éxito
        return redirect(url_for("dashboard"))  # Redirige al dashboard

    cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))  # Busca usuario por ID
    row = cur.fetchone()
    columnas = [desc[0] for desc in cur.description]
    usuario = dict(zip(columnas, row))  # Diccionario usuario
    cur.close()

    return render_template("edit.html", usuario=usuario)  # Muestra formulario de edición

# Editar usuario (perfil) - cuenta
@app.route("/edit_user/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user_account(id):
    cur = mysql.connection.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        fecha_nacimiento = request.form["fecha_nacimiento"]

        cur.execute("""
            UPDATE usuarios
            SET nombre = %s, apellido = %s, telefono = %s, email = %s, fecha_nacimiento = %s
            WHERE id = %s
        """, (nombre, apellido, telefono, email, fecha_nacimiento, id))

        mysql.connection.commit()
        cur.close()

        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for("account"))

    cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    row = cur.fetchone()
    columnas = [desc[0].lower() for desc in cur.description]  # Fuerza minúsculas
    usuario = dict(zip(columnas, row)) if row else None
    cur.close()

    return render_template("edit_user.html", usuario=usuario)

# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop("username", None)  # Elimina la variable de sesión username
    session.pop("nombre", None)    # Elimina la variable de sesión nombre
    session.pop("email", None)     # Elimina la variable de sesión email
    session.pop("rol", None)       # Elimina la variable de sesión rol
    return redirect(url_for("login"))  # Redirige al login


# ruta para la página de inicio
@app.route("/index")
def index():
    return render_template("index.html")

# Ejecuta la aplicación en modo debug
if __name__ == "__main__":
    app.run(debug=True)

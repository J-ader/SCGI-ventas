
# GestionMed

**GestionMed** es una plataforma web para la gestión y venta de medicamentos, diseñada para farmacias, droguerías y profesionales de la salud. Permite administrar usuarios, productos, inventario y ventas de manera segura y eficiente.

---

## Tabla de Contenidos

- [Equipo de Trabajo](#equipo-de-trabajo)
- [Descripción General](#descripción-general)
- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Seguridad](#seguridad)
- [Licencia](#licencia)

---

## Equipo de Trabajo

Este proyecto fue desarrollado por aprendices del programa **Tecnólogo en Análisis y Desarrollo de Software**, ficha **2834824**, del **Servicio Nacional de Aprendizaje (SENA)**.

**Integrantes del equipo:**
- Daniel José Meza Cruz
- Zaida Soralla Cortés Cortés
- Jader Luis Romero Montalvo
- Helmer Samir López Toscano

---

## Descripción General

GestionMed permite el registro y autenticación de usuarios, gestión de cuentas, panel de administración para usuarios con rol de administrador, y un catálogo de productos farmacéuticos. El sistema implementa buenas prácticas de seguridad y una interfaz moderna y responsiva.

---

## Características

- Registro y autenticación de usuarios
- Panel de administración para gestión de usuarios (solo administradores)
- Gestión de productos y catálogo visual
- Edición y eliminación de usuarios
- Protección CSRF manual en el formulario de inicio de sesión
- Sanitización de entradas para evitar XSS usando la librería `bleach`
- Mensajes flash para notificaciones de éxito y error
- Diseño responsivo y accesible

---

## Tecnologías Utilizadas

- **Backend:** Python, Flask, Flask-MySQLdb  
- **Frontend:** HTML5, CSS3, Bootstrap 5  
- **Base de datos:** MySQL  
- **Seguridad:** Werkzeug (hash de contraseñas), bleach (sanitización), CSRF manual en login  
- **Variables de entorno:** python-dotenv

---

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/SCGI-ventas.git
   cd SCGI-ventas
   ```

2. **Instala las dependencias:**

   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Configura la base de datos MySQL:**

   - Crea una base de datos y un usuario en MySQL.
   - Ejecuta el script para crear las tablas necesarias:

     ```bash
     mysql -u tu_usuario -p gestion_med < Database/Bd_script.sql
     ```

4. **Configura las variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

   ```env
   SECRET_KEY=tu_clave_secreta
   MYSQL_HOST=localhost
   MYSQL_USER=tu_usuario
   MYSQL_PASSWORD=tu_contraseña
   MYSQL_DB=gestion_med
   ```

---

## Configuración

- `SECRET_KEY`: Clave secreta para sesiones Flask.
- `MYSQL_*`: Datos de conexión a la base de datos MySQL.

---

## Estructura del Proyecto

```
SCGI-ventas/
│
├── .env
├── app.py
├── requirements.txt
├── static/
│   ├── productos.css
│   ├── login.css
│   ├── dashboard.css
│   ├── account.css
│   ├── edit.css
│   ├── registro.css
│   └── Media/
│       └── (imágenes y favicon)
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── registro.html
│   ├── productos.html
│   ├── dashboard.html
│   ├── account.html
│   ├── edit.html
│   └── edit_user.html
│
├── Database/
│   └── Bd_script.sql
└── ...
```

---

## Uso

1. Inicia la aplicación ejecutando:

   ```bash
   python app.py
   ```

2. Accede desde tu navegador a:

   ```
   http://localhost:5000/
   ```

**Funcionalidades principales:**

- Registro y login de usuarios.
- Panel de administración para gestionar usuarios (solo admin).
- Visualización y gestión de productos.
- Edición de perfil y cierre de sesión.

---

## Seguridad

- **CSRF:** Protección manual mediante tokens únicos por sesión en el formulario de login.
- **XSS:** Sanitización de entradas con `bleach`.
- **Contraseñas:** Hash seguro con `Werkzeug`.
- **Sesiones:** Protegidas con `SECRET_KEY`.

---

## Licencia

Este proyecto es solo para fines educativos y de demostración.

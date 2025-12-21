# Importamos las herramientas necesarias de Flask:
# - Flask: clase principal para crear la aplicación web
# - render_template: función para renderizar archivos HTML
# - request: objeto para acceder a los datos enviados por el usuario
# - session: para manejar sesiones de usuario
# - redirect: para redirigir a otras rutas
# - url_for: para generar URLs de forma dinámica..
from flask import Flask, render_template, request, session, redirect, url_for

# Creamos una instancia de la aplicación Flask
# __name__ indica el nombre del módulo actual, Flask lo usa para encontrar recursos
app = Flask(__name__)

# Configuración de la clave secreta para las sesiones
# En producción, esta debería ser una clave aleatoria y segura guardada en variables de entorno
app.config['SECRET_KEY'] = 'clave-secreta-temporal-para-desarrollo'

# Credenciales hardcodeadas (temporales, antes de implementar Supabase Auth)
VALID_EMAIL = "eder@gmail.com"
VALID_PASSWORD = "sandalias"

# Diccionario en memoria para almacenar usuarios registrados
# Formato: {email: password}
registered_users = {}

# Ruta de login que acepta GET (mostrar formulario) y POST (procesar login)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Obtenemos email y password del formulario
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # Validamos las credenciales (hardcodeadas o usuarios registrados)
        is_valid = False

        # Verificar credenciales hardcodeadas
        if email == VALID_EMAIL and password == VALID_PASSWORD:
            is_valid = True

        # Verificar usuarios registrados
        elif email in registered_users and registered_users[email] == password:
            is_valid = True

        if is_valid:
            # Credenciales correctas: guardamos en sesión y redirigimos
            session['logged_in'] = True
            session['user_email'] = email
            return redirect(url_for('home'))
        else:
            # Credenciales incorrectas: mostramos error
            return render_template("login.html",
                                   message="Invalid email or password.",
                                   status="error")

    # Si el usuario ya está logueado, redirigir al formulario
    if session.get('logged_in'):
        return redirect(url_for('home'))

    # GET request: mostrar página de login
    return render_template("login.html")

# Ruta de registro que acepta GET (mostrar formulario) y POST (procesar registro)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Obtenemos los datos del formulario
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        # Validación 1: Verificar que el email no esté vacío
        if not email:
            return render_template("register.html",
                                   message="Email is required.",
                                   status="error")

        # Validación 2: Verificar que el email tenga formato válido
        if "@" not in email or "." not in email:
            return render_template("register.html",
                                   message="Invalid email format.",
                                   status="error")

        # Validación 3: Verificar que la contraseña no esté vacía
        if not password:
            return render_template("register.html",
                                   message="Password is required.",
                                   status="error")

        # Validación 4: Verificar que las contraseñas coincidan
        if password != confirm_password:
            return render_template("register.html",
                                   message="Passwords do not match.",
                                   status="error")

        # Validación 5: Verificar que el email no esté ya registrado
        if email in registered_users:
            return render_template("register.html",
                                   message="Email already registered.",
                                   status="error")

        # Guardar el usuario en memoria
        registered_users[email] = password

        # Redirigir al login después de registrarse exitosamente
        return redirect(url_for('login'))

    # GET request: mostrar página de registro
    return render_template("register.html")

# Rutas del dashboard
@app.route("/dashboard/formulario", methods=["GET"])
def dashboard_formulario():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Renderizamos la página del formulario dentro del dashboard
    return render_template("formulario.html", current_page='formulario')

@app.route("/dashboard/preguntas", methods=["GET"])
def dashboard_preguntas():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Renderizamos la página de preguntas inteligentes
    return render_template("preguntas.html", current_page='preguntas')

# Definimos la ruta principal "/" que solo acepta peticiones GET
# Esta es la página de inicio que muestra el formulario vacío
@app.route("/", methods=["GET"])
def home():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Redirigimos al dashboard con el formulario
    return redirect(url_for('dashboard_formulario'))

# Definimos la ruta "/validate" que solo acepta peticiones POST
# Esta ruta procesa los datos del formulario enviado
@app.route("/validate", methods=["POST"])
def validate():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Obtenemos los valores del formulario usando request.form.get()
    # .strip() elimina espacios en blanco al inicio y final
    # Si el campo no existe, se usa "" como valor por defecto
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    age = request.form.get("age", "").strip()

    # VALIDACIÓN 1: Verificamos que el nombre no esté vacío
    if not name:
        return render_template("formulario.html",
                               message="Name is required.",
                               status="error",
                               current_page='formulario')

    # VALIDACIÓN 2: Verificamos que el email tenga formato básico válido
    # Debe contener "@" y "." para considerarse válido
    if "@" not in email or "." not in email:
        return render_template("formulario.html",
                               message="Invalid email format.",
                               status="error",
                               current_page='formulario')

    # VALIDACIÓN 3: Verificamos que la edad sea un número
    # .isdigit() devuelve True solo si todos los caracteres son dígitos
    if not age.isdigit():
        return render_template("formulario.html",
                               message="Age must be a number.",
                               status="error",
                               current_page='formulario')

    # Si todas las validaciones pasan, mostramos mensaje de éxito
    return render_template("formulario.html",
                           message="Form validated successfully!",
                           status="success",
                           current_page='formulario')

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    # Limpiamos toda la información de la sesión
    session.clear()
    # Redirigimos a la página de login
    return redirect(url_for('login'))

# Este bloque se ejecuta solo si el archivo se ejecuta directamente
# (no cuando se importa como módulo)
if __name__ == "__main__":
    # Iniciamos el servidor en modo debug
    # debug=True permite ver errores detallados y recarga automática
    # Usamos puerto 5001 porque el 5000 está ocupado por AirPlay en macOS
    app.run(debug=True, port=5001)
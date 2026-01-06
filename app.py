# Importamos las herramientas necesarias de Flask:
# - Flask: clase principal para crear la aplicación web
# - render_template: función para renderizar archivos HTML
# - request: objeto para acceder a los datos enviados por el usuario
# - session: para manejar sesiones de usuario
# - redirect: para redirigir a otras rutas
# - url_for: para generar URLs de forma dinámica..
from flask import Flask, render_template, request, session, redirect, url_for, make_response, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
import csv
from io import StringIO
import time
from datetime import datetime
import pytz

# Creamos una instancia de la aplicación Flask
# __name__ indica el nombre del módulo actual, Flask lo usa para encontrar recursos
app = Flask(__name__)

# Configuración de la clave secreta para las sesiones
# En producción, esta debería ser una clave aleatoria y segura guardada en variables de entorno
app.config['SECRET_KEY'] = 'clave-secreta-temporal-para-desarrollo'

# Inicialización de Firebase Admin SDK
# Ruta al archivo de credenciales de Firebase
cred_path = os.path.join(os.path.dirname(__file__), 'credentials', 'firebase-credentials.json')

# Inicializar Firebase solo si no ha sido inicializado antes y el archivo de credenciales existe
if not firebase_admin._apps and os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://rastreador-gps2-default-rtdb.firebaseio.com'
    })
elif not os.path.exists(cred_path):
    print(f"ADVERTENCIA: No se encontró el archivo de credenciales en {cred_path}")

# Credenciales hardcodeadas (temporales, antes de implementar Supabase Auth)
VALID_EMAIL = "luis@gmail.com"
VALID_PASSWORD = "admin123*"

# Diccionario en memoria para almacenar usuarios registrados
# Formato: {email: password}
registered_users = {}

# Función para convertir el formato de email de Firebase al formato normal (solo para visualización)
def convertir_email_firebase(email_firebase):
    """
    Convierte emails en formato Firebase a formato normal para visualización
    Ejemplo: lic_payanmz_at_gmail_com -> lic_payanmz@gmail.com
    NO modifica los datos en Firebase, solo convierte para mostrar
    """
    if not email_firebase or email_firebase == 'N/A':
        return email_firebase

    email = email_firebase
    # Reemplazar _at_ por @
    email = email.replace('_at_', '@')

    # Reemplazar extensiones comunes
    email = email.replace('_com', '.com')
    email = email.replace('_net', '.net')
    email = email.replace('_org', '.org')
    email = email.replace('_edu', '.edu')
    email = email.replace('_mx', '.mx')

    # Reemplazar _dot_ por . (si existe)
    email = email.replace('_dot_', '.')

    return email

# Función para convertir email normal a formato Firebase
def convertir_email_a_firebase(email_normal):
    """
    Convierte email normal a formato Firebase
    Ejemplo: lic_payanmz@gmail.com -> lic_payanmz_at_gmail_com
    """
    if not email_normal or email_normal == 'N/A':
        return email_normal

    email = email_normal.lower().strip()
    # Reemplazar @ por _at_
    email = email.replace('@', '_at_')

    # Reemplazar extensiones comunes
    email = email.replace('.com', '_com')
    email = email.replace('.net', '_net')
    email = email.replace('.org', '_org')
    email = email.replace('.edu', '_edu')
    email = email.replace('.mx', '_mx')

    # Reemplazar otros puntos por _dot_
    email = email.replace('.', '_dot_')

    return email

# Función para generar ID único basado en timestamp
def generar_id_pedido():
    """
    Genera un ID único para un pedido basado en timestamp
    Similar a los IDs de Shopify
    """
    return str(int(time.time() * 1000))

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
@app.route("/dashboard/consultar-datos", methods=["GET", "POST"])
def dashboard_consultar_datos():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Inicializamos la variable de datos
    datos = None
    error = None

    # Si es POST, consultamos los datos de Firebase
    if request.method == "POST":
        try:
            # Verificar si Firebase está inicializado
            if not firebase_admin._apps:
                error = "Firebase no está configurado. Por favor, agrega el archivo de credenciales en credentials/firebase-credentials.json"
            else:
                # Referencia a la ruta en Firebase Realtime Database
                ref = db.reference('/mi_shopify/puntos_clientes')

                # Obtenemos todos los datos
                datos_raw = ref.get()

                # Convertimos los datos a una lista de diccionarios
                if datos_raw:
                    datos = []
                    for key, value in datos_raw.items():
                        # Aseguramos que cada registro tenga los campos necesarios
                        # Convertimos el email del campo referido_por para visualización
                        referido_por_raw = value.get('referido_por', 'N/A')
                        referido_por_convertido = convertir_email_firebase(referido_por_raw)

                        datos.append({
                            'email': value.get('email', 'N/A'),
                            'nombre': value.get('nombre_inicial', 'N/A'),
                            'puntos_totales': value.get('puntos_totales', 0),
                            'referido_por': referido_por_convertido
                        })

                    # Ordenar por puntos_totales de mayor a menor
                    datos.sort(key=lambda x: x['puntos_totales'], reverse=True)
                else:
                    error = "No se encontraron datos en Firebase"
        except Exception as e:
            error = f"Error al consultar Firebase: {str(e)}"

    # Renderizamos la página de consultar datos con los datos obtenidos
    return render_template("consultar_datos.html",
                          current_page='consultar-datos',
                          datos=datos,
                          error=error)

@app.route("/dashboard/descargar-csv", methods=["GET"])
def descargar_csv():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        # Verificar si Firebase está inicializado
        if not firebase_admin._apps:
            return "Firebase no está configurado", 500

        # Referencia a la ruta en Firebase Realtime Database
        ref = db.reference('/mi_shopify/puntos_clientes')

        # Obtenemos todos los datos
        datos_raw = ref.get()

        # Crear el archivo CSV en memoria
        si = StringIO()
        writer = csv.writer(si)

        # Escribir encabezados
        writer.writerow(['Email', 'Nombre', 'Puntos Totales', 'Referido por'])

        # Escribir datos
        if datos_raw:
            # Convertir a lista y ordenar por puntos_totales
            datos_lista = []
            for key, value in datos_raw.items():
                # Convertimos el email del campo referido_por para visualización en CSV
                referido_por_raw = value.get('referido_por', 'N/A')
                referido_por_convertido = convertir_email_firebase(referido_por_raw)

                datos_lista.append({
                    'email': value.get('email', 'N/A'),
                    'nombre': value.get('nombre_inicial', 'N/A'),
                    'puntos_totales': value.get('puntos_totales', 0),
                    'referido_por': referido_por_convertido
                })

            # Ordenar por puntos_totales de mayor a menor
            datos_lista.sort(key=lambda x: x['puntos_totales'], reverse=True)

            # Escribir las filas ordenadas
            for dato in datos_lista:
                writer.writerow([
                    dato['email'],
                    dato['nombre'],
                    dato['puntos_totales'],
                    dato['referido_por']
                ])

        # Crear respuesta con el archivo CSV
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=puntos_clientes.csv"
        output.headers["Content-type"] = "text/csv"

        return output

    except Exception as e:
        return f"Error al generar CSV: {str(e)}", 500

@app.route("/dashboard/modificar-datos", methods=["GET"])
def dashboard_modificar_datos():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Renderizamos la página de modificar datos
    return render_template("modificar_datos.html", current_page='modificar-datos')

@app.route("/dashboard/verificar-email", methods=["POST"])
def verificar_email():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'No autorizado'}), 401

    try:
        # Verificar si Firebase está inicializado
        if not firebase_admin._apps:
            return jsonify({'success': False, 'message': 'Firebase no está configurado'}), 500

        # Obtener el email del request
        email_normal = request.json.get('email', '').strip()

        if not email_normal:
            return jsonify({'success': False, 'message': 'Email es requerido'}), 400

        # Convertir email a formato Firebase
        email_firebase = convertir_email_a_firebase(email_normal)

        # Buscar en Firebase
        ref = db.reference(f'/mi_shopify/puntos_clientes/{email_firebase}')
        cliente = ref.get()

        if cliente:
            return jsonify({
                'success': True,
                'message': 'Email encontrado',
                'nombre': cliente.get('nombre_inicial', 'N/A'),
                'puntos_actuales': cliente.get('puntos_totales', 0)
            })
        else:
            return jsonify({'success': False, 'message': 'El correo no existe'}), 404

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route("/dashboard/agregar-puntos", methods=["POST"])
def agregar_puntos():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'No autorizado'}), 401

    try:
        # Verificar si Firebase está inicializado
        if not firebase_admin._apps:
            return jsonify({'success': False, 'message': 'Firebase no está configurado'}), 500

        # Obtener datos del request
        email_normal = request.json.get('email', '').strip()
        razon = request.json.get('razon', '').strip()
        monto = request.json.get('monto', 0)

        # Validaciones
        if not email_normal:
            return jsonify({'success': False, 'message': 'Email es requerido'}), 400

        if not razon:
            return jsonify({'success': False, 'message': 'Razón es requerida'}), 400

        try:
            monto = int(monto)
            if monto <= 0:
                return jsonify({'success': False, 'message': 'El monto debe ser mayor a 0'}), 400
        except ValueError:
            return jsonify({'success': False, 'message': 'El monto debe ser un número válido'}), 400

        # Convertir email a formato Firebase
        email_firebase = convertir_email_a_firebase(email_normal)

        # Referencia al cliente
        ref_cliente = db.reference(f'/mi_shopify/puntos_clientes/{email_firebase}')
        cliente = ref_cliente.get()

        if not cliente:
            return jsonify({'success': False, 'message': 'El correo no existe'}), 404

        # Generar ID único para el pedido
        id_pedido = generar_id_pedido()

        # Obtener fecha actual en formato ISO con timezone
        tz = pytz.timezone('America/Mexico_City')
        fecha_actual = datetime.now(tz).isoformat()

        # Crear nuevo registro en historial_pedidos
        nuevo_pedido = {
            'Razon': razon,
            'fecha_compra': fecha_actual,
            'puntos_ganados': monto,
            'total_compra_mxn': monto
        }

        # Actualizar historial_pedidos
        ref_historial = db.reference(f'/mi_shopify/puntos_clientes/{email_firebase}/historial_pedidos/{id_pedido}')
        ref_historial.set(nuevo_pedido)

        # Actualizar puntos_totales
        puntos_actuales = cliente.get('puntos_totales', 0)
        nuevos_puntos_totales = puntos_actuales + monto

        ref_puntos = db.reference(f'/mi_shopify/puntos_clientes/{email_firebase}/puntos_totales')
        ref_puntos.set(nuevos_puntos_totales)

        return jsonify({
            'success': True,
            'message': f'Puntos agregados exitosamente. Nuevo total: {nuevos_puntos_totales}',
            'puntos_totales': nuevos_puntos_totales
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# Definimos la ruta principal "/" que solo acepta peticiones GET
# Esta es la página de inicio
@app.route("/", methods=["GET"])
def home():
    # Verificamos que el usuario esté logueado
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Redirigimos al dashboard con consultar datos
    return redirect(url_for('dashboard_consultar_datos'))

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
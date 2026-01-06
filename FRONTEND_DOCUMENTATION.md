# Documentación Frontend - Bosio Solutions Dashboard

## Estructura de Archivos

```
app_web1/
├── app.py                          # Backend Flask
└── templates/
    ├── login.html                  # Página de login
    ├── register.html              # Página de registro
    ├── dashboard.html             # Template base (sidebar + topbar)
    ├── consultar_datos.html       # Página para consultar datos (extiende dashboard)
    └── modificar_datos.html       # Página para modificar datos (extiende dashboard)
```

---

## Arquitectura del Frontend

### Sistema de Templates (Jinja2)

**Template Base:** `dashboard.html`
- Contiene la estructura fija: sidebar, topbar, content area
- Define un bloque `{% block content %}` para contenido dinámico
- Todas las páginas del dashboard extienden este template

**Templates Hijos:** `consultar_datos.html`, `modificar_datos.html`
- Extienden `dashboard.html`
- Sobrescriben el bloque `{% block content %}`
- Heredan sidebar y topbar automáticamente

---

## Prompt para Recrear el Frontend

### Prompt Principal

```
Crea un dashboard minimalista para una aplicación Flask con la siguiente estructura:

REQUISITOS:

1. LAYOUT FIJO (dashboard.html):
   - Sidebar izquierdo (250px de ancho, posición fija)
     * Background: #2c3e50
     * Items de navegación con hover effect
     * Resalta item activo usando parámetro current_page
     * Botón de logout en la parte inferior

   - Top Bar superior (60px de altura, posición fija)
     * Background: blanco
     * Muestra título: "Bosio Solutions"
     * Muestra email del usuario: {{ session.user_email }}

   - Content Area central
     * margin-left: 250px (ancho del sidebar)
     * margin-top: 60px (altura del topbar)
     * Solo esta área tiene scroll
     * Usa Jinja2 block: {% block content %}{% endblock %}

2. NAVEGACIÓN:
   - Items en sidebar:
     * "Consultar Datos" → /dashboard/consultar-datos
     * "Modificar Datos" → /dashboard/modificar-datos
   - Resalta item activo con clase .active
   - Usa condicional Jinja2: {% if current_page == 'consultar-datos' %}active{% endif %}

3. PÁGINA LOGIN (login.html):
   - Formulario centrado con campos: email y password
   - Toggle para mostrar/ocultar contraseña:
     * Icono SVG de ojo (gris, difuminado)
     * opacity: 0.4 por defecto, 0.7 en hover
     * Solo aparece cuando hay texto en el campo password
     * Al hacer clic alterna entre type="password" y type="text"
   - Link a página de registro
   - Mensaje de error/éxito dinámico

4. PÁGINAS DEL DASHBOARD:
   - consultar_datos.html: página para consultar datos de clientes desde Firebase
   - modificar_datos.html: página para modificar datos y agregar puntos manualmente
   - Ambas extienden dashboard.html

5. ESTILOS:
   - Diseño minimalista
   - Colores: sidebar oscuro (#2c3e50), contenido claro (#f4f6f8)
   - Transiciones suaves (0.2s ease)
   - Box shadows sutiles
   - Todo el CSS inline en los templates

6. BACKEND ROUTES:
   - /login (GET, POST)
   - /register (GET, POST)
   - / → redirige a /dashboard/consultar-datos
   - /dashboard/consultar-datos (GET, POST) → render consultar_datos.html con current_page='consultar-datos'
   - /dashboard/modificar-datos (GET) → render modificar_datos.html con current_page='modificar-datos'
   - /dashboard/verificar-email (POST) → verifica si un email existe en Firebase
   - /dashboard/agregar-puntos (POST) → agrega puntos a un cliente
   - /dashboard/descargar-csv (GET) → descarga datos de clientes en formato CSV
   - /logout → limpia sesión y redirige a login
```

---

## Prompt Específico por Componente

### 1. Dashboard Base Template

```
Crea un template base dashboard.html para Flask con:
- Sidebar fijo izquierdo (250px, background #2c3e50)
- Top bar fijo superior (60px, background blanco)
- Content area con margin-left: 250px y margin-top: 60px
- Navegación con items "Consultar Datos" y "Modificar Datos"
- Resalta item activo usando {% if current_page == 'X' %}active{% endif %}
- Botón de logout en parte inferior del sidebar
- Muestra "Bosio Solutions" en topbar y {{ session.user_email }}
- Define {% block content %}{% endblock %} para contenido dinámico
```

### 2. Login con Toggle de Contraseña

```
Crea login.html con:
- Formulario centrado (POST a /login)
- Campos: email (type="email") y password (type="password")
- Toggle para mostrar/ocultar contraseña:
  * Icono SVG de ojo dentro del input (posición absoluta a la derecha)
  * opacity: 0.4, hover: 0.7
  * display: none por defecto
  * Aparece solo cuando input.value.length > 0
  * Al hacer clic alterna entre type="password" y type="text"
- Usa oninput="handlePasswordInput()" para mostrar/ocultar icono
- Usa onclick="togglePassword()" para alternar visibilidad
- Link a /register
- Muestra mensaje de error/éxito si existe
```

---

## Especificaciones Técnicas de Componentes

### Sidebar
```css
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 250px;
    height: 100vh;
    background: #2c3e50;
    color: #ecf0f1;
    padding: 20px 0;
    z-index: 1000;
}

.nav-item {
    display: block;
    padding: 12px 20px;
    color: #ecf0f1;
    text-decoration: none;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}

.nav-item:hover {
    background: rgba(255,255,255,0.1);
    border-left-color: #3498db;
}

.nav-item.active {
    background: rgba(52,152,219,0.2);
    border-left-color: #3498db;
}
```

### Top Bar
```css
.topbar {
    position: fixed;
    left: 250px;
    top: 0;
    right: 0;
    height: 60px;
    background: white;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    align-items: center;
    padding: 0 30px;
    z-index: 999;
}
```

### Content Area
```css
.content {
    margin-left: 250px;
    margin-top: 60px;
    padding: 30px;
    min-height: calc(100vh - 60px);
}
```

### Toggle Password Icon
```css
.toggle-password {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    user-select: none;
    opacity: 0.4;
    display: none;
    transition: opacity 0.2s ease;
}

.toggle-password:hover {
    opacity: 0.7;
}

.toggle-password.show {
    display: block;
}
```

```javascript
function handlePasswordInput() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password');

    if (passwordInput.value.length > 0) {
        toggleIcon.classList.add('show');
    } else {
        toggleIcon.classList.remove('show');
    }
}

function togglePassword() {
    const passwordInput = document.getElementById('password');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
}
```

---

## Rutas Backend Necesarias

```python
# Rutas del dashboard
@app.route("/dashboard/consultar-datos", methods=["GET", "POST"])
def dashboard_consultar_datos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # ... lógica para consultar Firebase ...
    return render_template("consultar_datos.html",
                         current_page='consultar-datos',
                         datos=datos,
                         error=error)

@app.route("/dashboard/modificar-datos", methods=["GET"])
def dashboard_modificar_datos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("modificar_datos.html", current_page='modificar-datos')

# Ruta principal redirige al dashboard
@app.route("/", methods=["GET"])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('dashboard_consultar_datos'))

# API endpoints para modificar datos
@app.route("/dashboard/verificar-email", methods=["POST"])
def verificar_email():
    # ... lógica para verificar email en Firebase ...
    return jsonify({'success': True, 'nombre': ..., 'puntos_actuales': ...})

@app.route("/dashboard/agregar-puntos", methods=["POST"])
def agregar_puntos():
    # ... lógica para agregar puntos en Firebase ...
    return jsonify({'success': True, 'message': ..., 'puntos_totales': ...})
```

---

## Flujo de Navegación

```
1. Usuario accede a /
   → Redirige a /login (si no está logueado)

2. Usuario completa login
   → Redirige a /dashboard/consultar-datos

3. Dashboard carga con:
   - Sidebar con "Consultar Datos" (activo) y "Modificar Datos"
   - Top bar con "Bosio Solutions" y email del usuario
   - Content area muestra la página de consultar datos

4. Usuario hace clic en "Modificar Datos"
   → Navega a /dashboard/modificar-datos
   → Sidebar y topbar permanecen fijos
   → Solo content area cambia

5. Usuario hace clic en Logout
   → Limpia sesión
   → Redirige a /login
```

---

## Colores y Estilos

### Paleta de Colores
```
Sidebar Background:     #2c3e50
Sidebar Text:           #ecf0f1
Active Item:            #3498db (con rgba(52,152,219,0.2) de fondo)
Top Bar Background:     #ffffff
Top Bar Border:         #e0e0e0
Content Background:     #f4f6f8
Primary Button:         #007bff
Error Background:       #ffe0e0
Error Text:             #900
Success Background:     #e0ffe5
Success Text:           #060
```

### Tipografía
```
Font Family: Arial, sans-serif
Sidebar Title: 20px, font-weight: 600
Top Bar Title: 18px, font-weight: 500
Nav Items: 14-16px
Content: 16px base
```

### Espaciado
```
Sidebar Padding: 20px vertical, 0 horizontal
Nav Item Padding: 12px vertical, 20px horizontal
Top Bar Padding: 0 30px
Content Padding: 30px
Border Radius: 4-8px
```

---

## Características Especiales

### 1. Navegación Activa Dinámica
- Se pasa `current_page` desde cada ruta
- El template compara `current_page` con el nombre del item
- Si coincide, agrega clase `.active`

### 2. Toggle de Contraseña
- Icono SVG customizado (no emoji)
- Aparece/desaparece dinámicamente según contenido del input
- Opacidad reducida para diseño minimalista
- No cambia de icono al hacer clic

### 3. Template Inheritance
- Un solo lugar para modificar sidebar/topbar (dashboard.html)
- Páginas nuevas solo necesitan extender y definir content
- Consistencia automática en toda la aplicación

---

## Cómo Agregar una Nueva Página al Dashboard

1. **Crear template nuevo:**
```html
<!-- templates/nueva_pagina.html -->
{% extends "dashboard.html" %}

{% block content %}
<div class="container">
    <h2>Mi Nueva Página</h2>
    <p>Contenido aquí...</p>
</div>

<style>
    .container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
</style>
{% endblock %}
```

2. **Agregar ruta en app.py:**
```python
@app.route("/dashboard/nueva_pagina", methods=["GET"])
def dashboard_nueva_pagina():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("nueva_pagina.html", current_page='nueva_pagina')
```

3. **Agregar item en sidebar (dashboard.html):**
```html
<nav class="sidebar-nav">
    <a href="/dashboard/consultar-datos"
       class="nav-item {% if current_page == 'consultar-datos' %}active{% endif %}">
        Consultar Datos
    </a>
    <a href="/dashboard/modificar-datos"
       class="nav-item {% if current_page == 'modificar-datos' %}active{% endif %}">
        Modificar Datos
    </a>
    <a href="/dashboard/nueva_pagina"
       class="nav-item {% if current_page == 'nueva_pagina' %}active{% endif %}">
        Mi Nueva Página
    </a>
</nav>
```

---

## Testing Checklist

- [ ] Login muestra icono de ojo solo cuando hay texto en password
- [ ] Icono de ojo alterna visibilidad de contraseña
- [ ] Login exitoso redirige a dashboard con consultar datos
- [ ] Sidebar permanece fijo al hacer scroll
- [ ] Top bar permanece fijo al hacer scroll
- [ ] Solo content area tiene scroll
- [ ] Navegación entre páginas resalta item activo
- [ ] Email del usuario aparece en top bar
- [ ] Logout redirige a login
- [ ] Consultar datos muestra información de Firebase correctamente
- [ ] Modificar datos permite agregar puntos manualmente
- [ ] Mensajes de error/éxito se muestran correctamente

---

## Notas de Implementación

- Todo el CSS está inline en los templates (no hay archivo CSS externo)
- Las sesiones de Flask manejan la autenticación
- El parámetro `current_page` es crítico para la navegación activa
- Los templates usan Jinja2 syntax
- El servidor corre en puerto 5001 (puerto 5000 ocupado por AirPlay en macOS)

---

## Integración con Firebase (Nuevas Funcionalidades)

### Estructura Firebase Realtime Database

```
/mi_shopify/puntos_clientes/
    edersiordia_at_outlook_com/
        email: "edersiordia@outlook.com"
        nombre_inicial: "Eder"
        puntos_totales: 1700
        referido_por: "lic_payanmz_at_gmail_com"
        historial_pedidos/
            6543434547495/
                Razon: "Puntos por referidos"
                fecha_compra: "2025-05-02T20:23:01-07:00"
                puntos_ganados: 1000
                total_compra_mxn: 1000
```

**Nota:** Los emails en Firebase usan formato especial:
- `@` → `_at_`
- `.com` → `_com`
- `.net` → `_net`
- Ejemplo: `edersiordia@outlook.com` → `edersiordia_at_outlook_com`

---

## Página: Consultar Datos

### Descripción
Página para consultar y visualizar datos de clientes desde Firebase Realtime Database.

### Archivo
`templates/consultar_datos.html`

### Funcionalidades

1. **Consultar Todos los Datos**
   - Botón que extrae todos los clientes de `/mi_shopify/puntos_clientes`
   - Muestra datos en tabla HTML responsive

2. **Tabla de Datos**
   - Columnas: Email, Nombre, Puntos Totales, Referido por
   - Ordenamiento automático por Puntos Totales (mayor a menor)
   - Contador de total de registros
   - Hover effect en filas

3. **Descarga CSV**
   - Botón "Descargar CSV" debajo de la tabla
   - Descarga archivo `puntos_clientes.csv`
   - Datos ordenados igual que la tabla
   - Formato compatible con Excel

4. **Conversión de Emails**
   - Los emails en campo "Referido por" se convierten automáticamente
   - De formato Firebase: `lic_payanmz_at_gmail_com`
   - A formato normal: `lic_payanmz@gmail.com`
   - Solo para visualización (no modifica Firebase)

### Rutas Backend

```python
# Mostrar página y consultar datos
@app.route("/dashboard/consultar-datos", methods=["GET", "POST"])
def dashboard_consultar_datos():
    # GET: Muestra página vacía
    # POST: Consulta Firebase y muestra tabla

# Descargar CSV
@app.route("/dashboard/descargar-csv", methods=["GET"])
def descargar_csv():
    # Genera CSV en memoria y lo descarga
```

### Funciones Auxiliares

```python
def convertir_email_firebase(email_firebase):
    """
    Convierte emails de formato Firebase a formato normal
    Ejemplo: lic_payanmz_at_gmail_com -> lic_payanmz@gmail.com
    """
```

### Estilos Clave

```css
.btn-consultar {
    background: #3498db;
    color: white;
    padding: 12px 30px;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table thead {
    background: #2c3e50;
    color: white;
}

.btn-download {
    background: #27ae60;
    color: white;
}
```

---

## Página: Modificar Datos

### Descripción
Página para modificar datos de clientes en Firebase, con funcionalidad para agregar puntos manualmente.

### Archivo
`templates/modificar_datos.html`

### Funcionalidades

1. **Agregar Puntos Manualmente**
   - Botón principal que activa el formulario
   - Flujo de 3 pasos progresivos

2. **Step 1: Seleccionar Razón**
   - Dropdown con 3 opciones:
     - "Compra Manual"
     - "Puntos Regalados"
     - "Ingreso Manual"

3. **Step 2: Verificar Email**
   - Input para email del cliente (formato normal)
   - Botón "Verificar" que busca en Firebase
   - Si existe: Muestra nombre y puntos actuales
   - Si no existe: Mensaje de error

4. **Step 3: Agregar Monto**
   - Input numérico para cantidad de puntos
   - Muestra información del cliente
   - Botón "Agregar Puntos" para confirmar

5. **Actualización en Firebase**
   - Crea registro en `historial_pedidos` con ID único
   - Actualiza `puntos_totales` sumando los puntos nuevos
   - Fecha con timezone de México (America/Mexico_City)

### Rutas Backend

```python
# Mostrar página
@app.route("/dashboard/modificar-datos", methods=["GET"])
def dashboard_modificar_datos():
    # Renderiza página principal

# Verificar si email existe
@app.route("/dashboard/verificar-email", methods=["POST"])
def verificar_email():
    # Busca email en Firebase
    # Retorna JSON con success y datos del cliente

# Agregar puntos
@app.route("/dashboard/agregar-puntos", methods=["POST"])
def agregar_puntos():
    # Crea registro en historial_pedidos
    # Actualiza puntos_totales
    # Retorna JSON con success
```

### Funciones Auxiliares

```python
def convertir_email_a_firebase(email_normal):
    """
    Convierte email normal a formato Firebase
    Ejemplo: lic_payanmz@gmail.com -> lic_payanmz_at_gmail_com
    """

def generar_id_pedido():
    """
    Genera ID único basado en timestamp (milisegundos)
    Similar a IDs de Shopify
    """
```

### Ejemplo de Registro Creado

```json
{
    "6543446852789": {
        "Razon": "Compra Manual",
        "fecha_compra": "2026-01-04T20:39:58-07:00",
        "puntos_ganados": 300,
        "total_compra_mxn": 300
    }
}
```

### JavaScript (AJAX)

```javascript
// Verificar email (fetch POST)
const response = await fetch('/dashboard/verificar-email', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email })
});

// Agregar puntos (fetch POST)
const response = await fetch('/dashboard/agregar-puntos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        email: emailSeleccionado,
        razon: razonSeleccionada,
        monto: monto
    })
});
```

### Estilos Clave

```css
.btn-accion {
    background: #3498db;
    padding: 15px 30px;
}

.form-section {
    background: #f9f9f9;
    border: 1px solid #e0e0e0;
}

.cliente-info {
    background: #e8f5e9;
    border-left: 4px solid #27ae60;
}

.btn-success {
    background: #27ae60;
}
```

---

## Configuración Firebase

### Archivo de Credenciales
```
credentials/firebase-credentials.json
```

### Inicialización en app.py

```python
import firebase_admin
from firebase_admin import credentials, db

# Inicializar Firebase
cred_path = os.path.join(os.path.dirname(__file__), 'credentials', 'firebase-credentials.json')

if not firebase_admin._apps and os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://rastreador-gps2-default-rtdb.firebaseio.com'
    })
```

### Dependencias

```txt
Flask==3.0.0
gunicorn==21.2.0
firebase-admin==6.4.0
```

### .gitignore

```
credentials/
*.json
__pycache__/
venv_firebase/
```

---

## Navegación Actualizada del Dashboard

```
Sidebar:
1. Consultar Datos         → /dashboard/consultar-datos
2. Modificar Datos         → /dashboard/modificar-datos
3. Logout                  → /logout
```

---

## Nuevas Dependencias Python

```python
from flask import Flask, render_template, request, session, redirect, url_for, make_response, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
import csv
from io import StringIO
import time
from datetime import datetime
import pytz
```

---

## Testing Checklist Actualizado

### Consultar Datos
- [ ] Botón "Consultar Todos" extrae datos de Firebase
- [ ] Tabla muestra datos ordenados por puntos (mayor a menor)
- [ ] Emails en "Referido por" se muestran en formato normal
- [ ] Botón "Descargar CSV" genera archivo correctamente
- [ ] CSV contiene datos ordenados igual que la tabla
- [ ] Contador de registros muestra número correcto

### Modificar Datos
- [ ] Botón "Agregar Puntos Manualmente" muestra formulario
- [ ] Dropdown de razones funciona correctamente
- [ ] Verificación de email encuentra clientes existentes
- [ ] Error correcto cuando email no existe
- [ ] Agregar puntos crea registro en historial_pedidos
- [ ] puntos_totales se actualiza correctamente
- [ ] Formulario se resetea después de agregar puntos
- [ ] Enter funciona en inputs de email y monto

---

## Credenciales de Acceso (Testing)

```
Usuario: admin
Contraseña: admin
```

---

Actualizado: 2026-01-06
Proyecto: Bosio Solutions Dashboard
Framework: Flask + Jinja2 + Firebase Realtime Database
Puerto: 8000 (Gunicorn)

## Cambios Recientes (2026-01-06)
- Eliminadas páginas "Formulario" y "Preguntas Inteligentes"
- Dashboard ahora solo contiene "Consultar Datos" y "Modificar Datos"
- Redirección inicial apunta a /dashboard/consultar-datos

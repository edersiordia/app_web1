# Documentación Frontend - Bosio Solutions Dashboard

## Estructura de Archivos

```
app_web1/
├── app.py                          # Backend Flask
└── templates/
    ├── login.html                  # Página de login
    ├── register.html              # Página de registro
    ├── dashboard.html             # Template base (sidebar + topbar)
    ├── formulario.html            # Página del formulario (extiende dashboard)
    └── preguntas.html             # Página de preguntas (extiende dashboard)
```

---

## Arquitectura del Frontend

### Sistema de Templates (Jinja2)

**Template Base:** `dashboard.html`
- Contiene la estructura fija: sidebar, topbar, content area
- Define un bloque `{% block content %}` para contenido dinámico
- Todas las páginas del dashboard extienden este template

**Templates Hijos:** `formulario.html`, `preguntas.html`
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
     * "Formulario" → /dashboard/formulario
     * "Preguntas Inteligentes" → /dashboard/preguntas
   - Resalta item activo con clase .active
   - Usa condicional Jinja2: {% if current_page == 'formulario' %}active{% endif %}

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
   - formulario.html: formulario de validación con campos name, email, age
   - preguntas.html: página placeholder con mensaje "Coming soon"
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
   - / → redirige a /dashboard/formulario
   - /dashboard/formulario (GET) → render formulario.html con current_page='formulario'
   - /dashboard/preguntas (GET) → render preguntas.html con current_page='preguntas'
   - /validate (POST) → procesa formulario y regresa a formulario.html
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
- Navegación con items "Formulario" y "Preguntas Inteligentes"
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

### 3. Página de Formulario

```
Crea formulario.html que:
- Extiende dashboard.html con {% extends "dashboard.html" %}
- Sobrescribe {% block content %}
- Contiene formulario con campos: name, email, age
- POST a /validate
- Muestra mensajes de error/éxito si existen
- Contenedor centrado (max-width: 500px)
- Background blanco con box-shadow
```

### 4. Página Placeholder

```
Crea preguntas.html que:
- Extiende dashboard.html
- Muestra título "Preguntas Inteligentes"
- Texto: "This feature is coming soon..."
- Contenedor centrado con estilos similares a formulario.html
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
@app.route("/dashboard/formulario", methods=["GET"])
def dashboard_formulario():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("formulario.html", current_page='formulario')

@app.route("/dashboard/preguntas", methods=["GET"])
def dashboard_preguntas():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("preguntas.html", current_page='preguntas')

# Ruta principal redirige al dashboard
@app.route("/", methods=["GET"])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('dashboard_formulario'))

# Validación de formulario
@app.route("/validate", methods=["POST"])
def validate():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # ... lógica de validación ...

    return render_template("formulario.html",
                         message="...",
                         status="...",
                         current_page='formulario')
```

---

## Flujo de Navegación

```
1. Usuario accede a /
   → Redirige a /login (si no está logueado)

2. Usuario completa login
   → Redirige a /dashboard/formulario

3. Dashboard carga con:
   - Sidebar con "Formulario" (activo) y "Preguntas Inteligentes"
   - Top bar con "Bosio Solutions" y email del usuario
   - Content area muestra formulario

4. Usuario hace clic en "Preguntas Inteligentes"
   → Navega a /dashboard/preguntas
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
<a href="/dashboard/nueva_pagina"
   class="nav-item {% if current_page == 'nueva_pagina' %}active{% endif %}">
    Mi Nueva Página
</a>
```

---

## Testing Checklist

- [ ] Login muestra icono de ojo solo cuando hay texto en password
- [ ] Icono de ojo alterna visibilidad de contraseña
- [ ] Login exitoso redirige a dashboard con formulario
- [ ] Sidebar permanece fijo al hacer scroll
- [ ] Top bar permanece fijo al hacer scroll
- [ ] Solo content area tiene scroll
- [ ] Navegación entre páginas resalta item activo
- [ ] Email del usuario aparece en top bar
- [ ] Logout redirige a login
- [ ] Formulario valida correctamente
- [ ] Mensajes de error/éxito se muestran correctamente

---

## Notas de Implementación

- Todo el CSS está inline en los templates (no hay archivo CSS externo)
- Las sesiones de Flask manejan la autenticación
- El parámetro `current_page` es crítico para la navegación activa
- Los templates usan Jinja2 syntax
- El servidor corre en puerto 5001 (puerto 5000 ocupado por AirPlay en macOS)

---

Creado: 2025-12-20
Proyecto: Bosio Solutions Dashboard
Framework: Flask + Jinja2

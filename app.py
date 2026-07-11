""" import mysql.connector
import requests__template,requests

app = Flask . (__ ciccolato __)


def  obtener_conexion ():
    return mysql.connecctor.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "cioccolato"
    ) 
    
    import requests
    from flask import Flask, render_template, request

    app = Flask(__name__)

# ─── RUTA 1: EXPLICACIÓN DE RUTA SIMPLE  ───
# Cuando entran a http://localhost:5000/ simplemente ven un saludo
    app.route('/')
    def inicio():
        texto_bienvenida = "¡Servidor Flask Activo! Ve a /registro para probar el formulario."
        return render_template('inicio.html', mensaje=texto_bienvenida)


# ─── RUTA 2: EL PLATO FUERTE (GET Y POST) ───
# Le añadimos el argumento 'methods' para que la ruta sepa manejar ambas intenciones
    app.route('/registro', methods=['GET', 'POST'])
    def registro():
    
    # CASO A: El usuario solo quiere VER la página (Petición GET)
        if request.method == 'GET':
            return render_template('registro.html')
    
    # CASO B: El usuario llenó los campos y le dio al botón "Enviar" (Petición POST)
        elif request.method == 'POST':
        # Capturamos los datos que viajan ocultos usando el atributo 'name' del HTML
            nombre_alumno = request.form.get('nombre_usuario')
        correo_alumno = request.form.get('correo_usuario')
        
        # Validamos rápido en Python si no los enviaron vacíos
        if nombre_alumno and correo_alumno:
            # Enviamos una respuesta confirmando que Python atrapó los datos
            mensaje_confirmacion = "¡Registro exitoso!" 
            detalles=f"Nombre: {nombre_alumno}</p><p>Correo: {correo_alumno}"
            enlace_inicio = "Registrar otro usuario"
            return render_template('registro_confirmacion.html', mensaje=mensaje_confirmacion, detalles=detalles, enlace=enlace_inicio)
        else:
            mensaje_error = "Error: Todos los campos son obligatorios."
            mensajeEnlace = "Volver al formulario"
            return render_template('registro_confirmacion.html', mensaje=mensaje_error, enlace=mensajeEnlace)
# ─── RUTA 3: CONSUMO DE API EXTERNA ───
    app.route('/perfil')
    def mostrar_perfil():
    # Enlace público de la API
        enlace_api = "https://randomuser.me/api/"
    
    # 1. Flask hace la petición GET a internet
    peticion_internet = requests.get(enlace_api)
    
    # 2. Transformamos la respuesta en un diccionario de Python
    datos_json = peticion_internet.json()
    print(datos_json) # Imprime el JSON completo en la terminal para que lo veamos
    # 3. "Desarmamos" el JSON buscando las llaves específicas (Repaso de diccionarios)
    datos_crudos_usuario = datos_json['results'][0]
    
    # Creamos un diccionario limpio con lo que queremos mandarle al HTML
    informacion_filtrada = {
        "nombre": f"{datos_crudos_usuario['name']['first']} {datos_crudos_usuario['name']['last']}",
        "pais": datos_crudos_usuario['location']['country'],
        "correo": datos_crudos_usuario['email'],
        "foto": datos_crudos_usuario['picture']['large'] # Esto es un enlace a una imagen (.jpg)
    }
    
    # 4. Renderizamos el template y le pasamos el diccionario con el nombre de 'info'
    return render_template('perfil.html', info=informacion_filtrada)
    if __name__ == '__main__':
    # Encendemos el servidor en modo de depuración técnica
        app.run(debug=True, port=5000)
        
        
        
         """
import os
import sqlite3  # 💾 ¡Cambiamos mysql por sqlite3!
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_Luis'

# 📁 Conexión universal: crea un archivo local que viaja directo a Render
def obtener_conexion():
    # En SQLite, 'connect' crea el archivo automáticamente si no existe
    conexion = sqlite3.connect('cioccolato.sqlite ')
    # Activamos esto para poder acceder a los datos por índice como hacíamos en MySQL
    return conexion

# ==========================================
# 🔐 GESTIÓN DE ACCESO (LOGIN / LOGOUT)
# ==========================================
@app.route('/login', methods=['POST'])
def login():
    usuario_ingresado = request.form.get('usuario')
    clave_ingresada = request.form.get('clave')
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # 🔍 En SQLite cambiamos los '%s' por '?'
    sql = "SELECT id, usuario FROM usuarios WHERE usuario = ? AND clave = ?"
    cursor.execute(sql, (usuario_ingresado, clave_ingresada))
    usuario_encontrado = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    if usuario_encontrado:
        session['usuario'] = usuario_encontrado[1]
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('home'))

# ==========================================
# 🏠 RUTA PRINCIPAL (READ)
# ==========================================
@app.route('/')
def home():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # 🚨 TRUCO DE MAÑANA: Creamos las tablas automáticamente si es la primera vez que corre en Render
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            clave TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            imagen TEXT
            
        )
    """)
    
    # Insertamos el admin por defecto si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES ('admin', '1234')")
        conexion.commit()

    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    es_admin = 'usuario' in session
    return render_template('index.html', inventario=productos_db, es_admin=es_admin)

# ==========================================
# 📥 OPERACIÓN: CREATE
# ==========================================
@app.route('/nuevo-producto', methods=['POST'])
def nuevo_producto():
    if 'usuario' not in session:
        return "Acceso denegado.", 403

    txt_nombre = request.form.get('nombre')
    txt_precio = request.form.get('precio')
    txt_stock = request.form.get('stock')
    txt_categoria = request.form.get('categoria')
    imagen = request.files.get('imagen')
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    if imagen and imagen.filename != '':
        ruta_imagen = f'static/imagenes/{imagen.filename}'
        imagen.save(ruta_imagen)
        # Usamos '?' para SQLite
        comando = "INSERT INTO productos (nombre, precio, stock, categoria, imagen) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(comando, (txt_nombre, txt_precio, txt_stock, txt_categoria, ruta_imagen))
    else:
        comando = "INSERT INTO productos (nombre, precio, stock, categoria) VALUES (?, ?, ?, ?)"
        cursor.execute(comando, (txt_nombre, txt_precio, txt_stock, txt_categoria))
    
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('home'))

# ==========================================
# 🛠️ OPERACIÓN: UPDATE (MOSTRAR)
# ==========================================
@app.route('/update/<int:id_producto>')
def mostrar_editar(id_producto):
    if 'usuario' not in session:
        return "Acceso denegado.", 403

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "SELECT id, nombre, precio, stock, categoria, imagen FROM productos WHERE id = ?"
    cursor.execute(sql, (id_producto,))
    producto = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    return render_template('editar.html', producto=producto)

# ==========================================
# 💾 OPERACIÓN: UPDATE (GUARDAR)
# ==========================================
@app.route('/actualizar/<int:id_producto>', methods=['POST'])
def actualizar_producto(id_producto):
    if 'usuario' not in session:
        return "Acceso denegado.", 403

    nuevo_nombre = request.form.get('nombre')
    nuevo_precio = request.form.get('precio')
    nuevo_stock = request.form.get('stock')
    nueva_categoria = request.form.get('categoria')
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    comando = """
        UPDATE productos 
        SET nombre = ?, precio = ?, stock = ?, categoria = ? 
        WHERE id = ?
    """
    cursor.execute(comando, (nuevo_nombre, nuevo_precio, nuevo_stock, nueva_categoria, id_producto))
    
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('home'))

# ==========================================
# ❌ OPERACIÓN: DELETE
# ==========================================
@app.route('/eliminar/<int:id_producto>')
def eliminar_producto(id_producto):
    if 'usuario' not in session:
        return "Acceso denegado.", 403

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "DELETE FROM productos WHERE id = ?"
    cursor.execute(sql, (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
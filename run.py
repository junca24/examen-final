from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('productos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla si no existe
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                estado TEXT NOT NULL,
                clasificacion TEXT NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        conn.commit()

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Obtener todos los productos
@app.route('/productos')
def obtener_productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return jsonify([dict(row) for row in productos])

# Crear un nuevo producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO productos (nombre, estado, clasificacion, precio) VALUES (?, ?, ?, ?)',
        (data['nombre'], data['estado'], data['clasificacion'], data['precio'])
    )
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Producto creado'}), 201

# Actualizar un producto
@app.route('/productos/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'UPDATE productos SET nombre = ?, estado = ?, clasificacion = ?, precio = ? WHERE id_producto = ?',
        (data['nombre'], data['estado'], data['clasificacion'], data['precio'], id_producto)
    )
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Producto actualizado'})

# Eliminar un producto
@app.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    conn = get_db_connection()
    conn.execute('DELETE FROM productos WHERE id_producto = ?', (id_producto,))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Producto eliminado'})

# Ejecutar el servidor y crear la base de datos si no existe
if __name__ == '__main__':
    init_db()  # crea la tabla si no existe
    app.run(debug=True)

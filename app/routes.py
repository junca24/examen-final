from flask import Blueprint, render_template, request, redirect, url_for
from .models import Producto
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@main.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    estado = request.form['estado']
    clasificacion = request.form['clasificacion']
    precio = float(request.form['precio'])

    nuevo = Producto(nombre=nombre, estado=estado, clasificacion=clasificacion, precio=precio)
    db.session.add(nuevo)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    producto = Producto.query.get_or_404(id)

    producto.nombre = request.form['nombre']
    producto.estado = request.form['estado']
    producto.clasificacion = request.form['clasificacion']
    producto.precio = float(request.form['precio'])

    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/eliminar/<int:id>')
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('main.index'))

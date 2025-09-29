from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..data.mysqlConexion import get_db

productos_ct = Blueprint("productos", __name__)

@productos_ct.route('/listar_productos_agregados')
def listar_productos():
    if 'islogued' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        cursor.close()
        return render_template('productos.html', productos=productos, user=session.get('email'))
    else:
        flash("Access denied. Please log in.", "error")
        return redirect(url_for('login.sigin'))
    
@productos_ct.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if 'islogued' in session and session.get('id_role') == 2:
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            categoria = request.form.get('categoria')
            precio = request.form.get('precio')
            cantidad = request.form.get('cantidad')
            
            if not nombre or not categoria or not precio or not cantidad:
                flash("All fields are required.", "error")
                return redirect(url_for('productos.agregar_producto'))
            
            try:
                db = get_db()
                cursor = db.cursor()
                args = (categoria, nombre, float(precio), int(cantidad))
                cursor.callproc('insertarProductos', args)
                db.commit()
                cursor.close()
                flash("Product added successfully!", "success")
                return redirect(url_for('productos.listar_productos'))
            except Exception as e:
                flash(f"Error adding product: {e}", "error")
                return redirect(url_for('productos.insertar_producto'))
        
        return render_template('insertar_producto.html')
    else:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('login.sigin'))
    
@productos_ct.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if 'islogued' in session and session.get('id_role') == 2:
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id,))
            db.commit()
            cursor.close()
            flash("Product deleted successfully!", "success")
        except Exception as e:
            flash(f"Error deleting product: {e}", "error")
        return redirect(url_for('productos.listar_productos'))
    else:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('login.sigin'))
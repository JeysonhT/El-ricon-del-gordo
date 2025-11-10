from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..data.mysqlConexion import get_db
import json
from datetime import datetime, timedelta


productos_ct = Blueprint("productos", __name__)


@productos_ct.route("/listar_productos_agregados")
def listar_productos():
    if "islogued" in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        return render_template(
            "productos.html", productos=productos, user=session.get("email")
        )
    else:
        flash("Access denied. Please log in.", "error")
        return redirect(url_for("login.sigin"))


@productos_ct.route("/productos_graficas")
def productos_graficas():
    if "islogued" in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT nombre, precio FROM productos ORDER BY precio DESC")
        productos = cursor.fetchall()
        cursor.close()
        
        nombres = [producto['nombre'] for producto in productos]
        precios = [float(producto['precio']) for producto in productos]
        
        return render_template(
            "productos_graficas.html", 
            nombres=json.dumps(nombres), 
            precios=json.dumps(precios)
        )
    else:
        flash("Access denied. Please log in.", "error")
        return redirect(url_for("login.sigin"))


@productos_ct.route("/productos_por_fecha")
def productos_por_fecha():
    if "islogued" in session:
        try:
            db = get_db()
            cursor = db.cursor()

            # Get data for the last 7 days
            today = datetime.now()
            last_week = today - timedelta(days=7)
            
            query = """
                SELECT DATE(fecha) as entry_date, COUNT(*) as product_count
                FROM productos
                WHERE fecha BETWEEN %s AND %s
                GROUP BY DATE(fecha)
                ORDER BY DATE(fecha) ASC
            """
            
            cursor.execute(query, (last_week.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
            
            product_data = cursor.fetchall()
            cursor.close()

            # Prepare data for the chart
            labels = [data['entry_date'].strftime('%Y-%m-%d') for data in product_data]
            values = [data['product_count'] for data in product_data]

            return render_template(
                "productos_por_fecha.html",
                labels=json.dumps(labels),
                values=json.dumps(values)
            )
        except Exception as e:
            flash(f"Error loading product data: {e}", "error")
            return redirect(url_for("admin.admin_dashboard"))
    else:
        flash("Access denied. Please log in.", "error")
        return redirect(url_for("login.sigin"))


@productos_ct.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():
    if "islogued" in session and session.get("id_role") == 2:
        if request.method == "POST":
            nombre = request.form.get("nombre")
            categoria = request.form.get("categoria")
            precio = request.form.get("precio")
            cantidad = request.form.get("cantidad")
            fecha = request.form.get("fecha")

            if not nombre or not categoria or not precio or not cantidad or not fecha:
                flash("All fields are required.", "error")
                return redirect(url_for("productos.agregar_producto"))

            try:
                db = get_db()
                cursor = db.cursor()
                args = (categoria, nombre, float(precio), int(cantidad), fecha)
                cursor.callproc("insertarProductos", args)
                db.commit()
                cursor.close()
                flash("Product added successfully!", "success")
                return redirect(url_for("productos.listar_productos"))
            except Exception as e:
                flash(f"Error adding product: {e}", "error")
                return redirect(url_for("productos.agregar_producto"))

        return render_template("insertar_producto.html")
    else:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for("login.sigin"))


@productos_ct.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if "islogued" in session and session.get("id_role") == 2:
        db = get_db()
        cursor = db.cursor()

        if request.method == "POST":
            nombre = request.form.get("nombre")
            categoria = request.form.get("categoria")
            precio = request.form.get("precio")
            cantidad = request.form.get("cantidad")
            fecha = request.form.get("fecha")

            if not nombre or not categoria or not precio or not cantidad or not fecha:
                flash("All fields are required.", "error")
                return redirect(url_for("productos.editar_producto", id=id))

            try:
                args = (id, categoria, nombre, float(precio), int(cantidad), fecha)
                cursor.callproc("actualizar_producto", args)
                db.commit()
                flash("Product updated successfully!", "success")
                return redirect(url_for("productos.listar_productos"))
            except Exception as e:
                flash(f"Error updating product: {e}", "error")
                return redirect(url_for("productos.editar_producto", id=id))
            finally:
                cursor.close()

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
        producto = cursor.fetchone()
        cursor.close()

        if producto is None:
            flash("Product not found.", "error")
            return redirect(url_for("productos.listar_productos"))

        return render_template("insertar_producto.html", producto=producto)
    else:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for("login.sigin"))


@productos_ct.route("/eliminar_producto/<int:id>", methods=["POST"])
def eliminar_producto(id):
    if "islogued" in session and session.get("id_role") == 2:
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
            db.commit()
            cursor.close()
            flash("Product deleted successfully!", "success")
        except Exception as e:
            flash(f"Error deleting product: {e}", "error")
        return redirect(url_for("productos.listar_productos"))
    else:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for("login.sigin"))

from flask_mysqldb import MySQL
from flask import current_app, g

import threading

# pool de conexiones para manejar múltiples hilos
mysql = MySQL()
            
def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connection
            current_app.logger.debug("Conexión MySQL establecida")
        except Exception as e:
            current_app.logger.error(f"Error al conectar con MySQL: {e}")
            raise
    
    return g.db

def get_cursor():
    """
    Obtiene un cursor desde la conexión actual
    """
    db = get_db()
    try:
        cursor = db.cursor()
        return cursor
    except Exception as e:
        current_app.logger.error(f"Error al obtener cursor: {e}")
        raise

def close_db(e=None):
    """
    Cierra la conexión de base de datos al final del request
    """
    db = g.pop('db', None)

    if db is not None:
        try:
            db.close()
            current_app.logger.debug("Conexión MySQL cerrada")
        except Exception as e:
            current_app.logger.error(f"Error al cerrar conexión: {e}")

def init_app(app):
    """
    Configura la extensión MySQL con la aplicación
    """
    mysql.init_app(app)
    #app.teardown_appcontext(close_db)
from flask import Flask
from .data.mysqlConexion import init_app

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    
    app.secret_key = 'clave_secreta'
    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'developer'
    app.config['MYSQL_PASSWORD'] = 'pandeplatano3'
    app.config['MYSQL_DB'] = 'Ventas'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    app.config['MYSQL_CONNECT_TIMEOUT'] = 30  # Tiempo de espera para la conexión en segundos
    app.config['MYSQL_READ_TIMEOUT'] = 10     # Tiempo de espera para leer
    app.config['MYSQL_WRITE_TIMEOUT'] = 10    # Tiempo de espera para escribir
    app.config['MYSQL_AUTO_COMMIT'] = True  # Habilitar auto-commit para evitar problemas de bloqueo
    app.config['MYSQL_POOL_SIZE'] = 5  # Tamaño del pool de conexiones
    app.config['MYSQL_POOL_TIMEOUT'] = 30  # Tiempo de espera para obtener una conexión del pool
    
    # Configuraciones de la aplicación
    init_app(app)
    
    from .controllers.UserController import user_ct
    from .controllers.LoginController import login_ct
    from .controllers.homeController import home_ct
    from .controllers.AdminController import admin_ct
    from .controllers.ProductosController import productos_ct
    
    app.register_blueprint(user_ct)
    app.register_blueprint(login_ct)
    app.register_blueprint(home_ct)
    app.register_blueprint(admin_ct)
    app.register_blueprint(productos_ct)
    
    return app
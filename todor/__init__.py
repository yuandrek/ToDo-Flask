

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# crear la extensión
db = SQLAlchemy()

# instancia (sirve para conexión a base de datos, testear)
def create_app():
    
    # Crear la aplicación
    app = Flask(__name__)

    # Configuración del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        # configurar la base de datos SQLite, relativa a la carpeta de instancia de la aplicación
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"
    )

    # Inicializar la aplicación con la extensión
    db.init_app(app) 

    # Registrar Blueprint
    from . import todo
    app.register_blueprint(todo.bp)

    from . import auth
    app.register_blueprint(auth.bp)


    # ruta
    @app.route('/')
    # vista
    def index():
        return render_template('index.html')
    
    # permite migrar todos los modelos creados en la aplicación a la base de datos
    with app.app_context():
      db.create_all()
    
    return app 
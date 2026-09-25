"""
Application factory del frontend.

CAMBIO CLAVE respecto al Taller 2: este servicio ya NO se conecta a
ninguna base de datos. Su única fuente de datos es la API (servicio
'api'), a través de peticiones HTTP.
"""

from flask import Flask

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)

    # TODO 1: Carga la configuración: app.config.from_object(config_class)

    # TODO 2: Importa el blueprint 'main' desde .routes y regístralo:
    #         from .routes import main
    #         app.register_blueprint(main)

    return app

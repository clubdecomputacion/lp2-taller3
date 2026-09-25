"""Configuración del frontend Flask."""

import os


class Config:
    # TODO 1: lee SECRET_KEY desde la variable de entorno del mismo nombre,
    #         con un valor por defecto para desarrollo local.
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave")

    # TODO 2: lee API_URL desde la variable de entorno definida en
    #         docker-compose.yml (host "api", puerto 8000). Deja un valor
    #         por defecto que sirva si ejecutas este servicio SIN Docker,
    #         directamente en tu máquina (http://localhost:8000).
    API_URL = os.environ.get("API_URL", "http://localhost:8000")

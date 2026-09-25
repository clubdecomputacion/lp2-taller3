"""
Cliente HTTP hacia el servicio 'api'.

Este módulo concentra TODAS las llamadas de red hacia la API, para que
routes.py no tenga que preocuparse por URLs, timeouts o códigos de estado.
Es el equivalente, en esta arquitectura, a lo que antes hacía el ORM
directamente: "conseguir los datos", solo que ahora viajan por HTTP en
lugar de SQL.
"""

import requests
from flask import current_app

TIMEOUT = 5  # segundos máximo de espera por respuesta de la API


def obtener_productos(categoria_id=None):
    """Retorna la lista de productos (dicts) desde la API.

    TODO 1: Construye la URL completa:
            url = f"{current_app.config['API_URL']}/productos/"
    TODO 2: Arma un diccionario de parámetros; si categoria_id no es None,
            agrégalo como {"categoria_id": categoria_id}, si es None usa {}.
    TODO 3: Haz la petición:
            respuesta = requests.get(url, params=parametros, timeout=TIMEOUT)
    TODO 4: Si respuesta.status_code == 200, retorna respuesta.json()
            En cualquier otro caso, retorna una lista vacía [] (para que
            la página no se rompa si la API está caída).
    """
    pass


def obtener_producto(sku):
    """Retorna un producto (dict) por su SKU, o None si no existe.

    TODO 5: Construye la URL:
            url = f"{current_app.config['API_URL']}/productos/{sku}"
    TODO 6: Haz la petición GET con requests.get(url, timeout=TIMEOUT)
    TODO 7: Si respuesta.status_code == 200, retorna respuesta.json()
            Si es 404 (u otro código), retorna None.
    """
    pass


def obtener_categorias():
    """Retorna la lista de categorías (dicts) desde la API.

    TODO 8: Igual que obtener_productos() pero apuntando a
            f"{current_app.config['API_URL']}/categorias/" y sin parámetros.
    """
    pass

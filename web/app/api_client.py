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
    """Retorna la lista de productos (dicts) desde la API. """
    
    url = f"{current_app.config['API_URL']}/productos/"
    parametros = {}
    if categoria_id is not None:
        parametros["categoria_id"] = categoria_id
        
    try:
        respuesta = requests.get(url, params=parametros, timeout=TIMEOUT)
        if respuesta.status_code == 200:
            return respuesta.json()
    except requests.RequestException:
        return []

    return [] 


def obtener_producto(sku):
    """Retorna un producto (dict) por su SKU, o None si no existe. """
    
    url = f"{current_app.config['API_URL']}/productos/{sku}"
    
    try:
        respuesta = requests.get(url, timeout=TIMEOUT)
        if respuesta.status_code == 200:
            return respuesta.json()
    except requests.RequestException:
        return None

    return None


def obtener_categorias():
    """Retorna la lista de categorías (dicts) desde la API.
"""
    
    url = f"{current_app.config['API_URL']}/categorias/"
    try:
        respuesta = requests.get(url, timeout=TIMEOUT)
        if respuesta.status_code == 200:
            return respuesta.json()
    except requests.RequestException:
        return []

    return []   
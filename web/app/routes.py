"""
Rutas del frontend.

CAMBIO CLAVE respecto al Taller 2: aquí NO hay consultas ORM
(Producto.query...). Todo pasa por funciones de api_client, que a su vez
hacen peticiones HTTP al servicio 'api'. Esta vista Flask solo se encarga
de pedir datos y renderizar HTML: es un "cliente" de la API, igual que lo
sería una app móvil o un frontend en React.
"""

from flask import Blueprint, abort, render_template, request

from . import api_client

main = Blueprint("main", __name__)


@main.route("/")
def index():
    categoria_id = request.args.get("categoria", type=int)

    # TODO 1: productos = api_client.obtener_productos(categoria_id)
    # TODO 2: categorias = api_client.obtener_categorias()
    # TODO 3: render_template("index.html", productos=productos,
    #                         categorias=categorias, categoria_id=categoria_id)
    pass


@main.route("/producto/<sku>")
def detalle(sku):
    # TODO 4: producto = api_client.obtener_producto(sku)
    # TODO 5: si producto es None, abort(404)
    # TODO 6: render_template("detalle.html", producto=producto)
    pass


@main.route("/categorias")
def categorias():
    # TODO 7: categorias = api_client.obtener_categorias()
    # TODO 8: render_template("categorias.html", categorias=categorias)
    pass

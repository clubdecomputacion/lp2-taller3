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
    casa_activa = request.args.get("casa")

    productos = api_client.obtener_productos(categoria_id)
    categorias = api_client.obtener_categorias()
    casas = sorted(
        {producto["marca"] for producto in productos if producto.get("marca")}
    )
    if casa_activa:
        productos = [
            producto for producto in productos
            if producto.get("marca") == casa_activa
        ]

    return render_template(
        "index.html",
        productos=productos,
        categorias=categorias,
        categoria_id=categoria_id,
        casas=casas,
        casa_activa=casa_activa,
    )


@main.route("/producto/<sku>")
def detalle(sku):
    producto = api_client.obtener_producto(sku)
    if producto is None:
        abort(404)
    return render_template("detalle.html", producto=producto)
    


@main.route("/categorias")
def categorias():
    categorias = api_client.obtener_categorias()
    return render_template("categorias.html", categorias=categorias)
    

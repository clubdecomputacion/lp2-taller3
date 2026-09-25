"""
Script de carga inicial (seed) de la base de datos.

A diferencia del Taller 2 (que usaba comandos "flask seed-db"), aquí es un
script independiente porque este servicio no usa el CLI de Flask.

Se ejecuta DENTRO del contenedor de la API:

    docker compose exec api python -m app.seed
"""

import json
import os

from .database import Base, SessionLocal, engine
from .models import Categoria, Producto

RUTA_PRODUCTOS = os.path.join(os.path.dirname(__file__), "..", "data", "productos.json")


def cargar_datos():
    # Se asegura de que las tablas existan (por si se corre antes que main.py).
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # TODO 1: Abre RUTA_PRODUCTOS con encoding="utf-8" y usa json.load()
        #         para obtener la lista de productos.
        # datos = ...

        # TODO 2: Por cada item en 'datos':
        #   a) Busca la categoría por nombre:
        #        categoria = db.query(Categoria).filter_by(
        #            nombre=item["categoria"]).first()
        #   b) Si no existe, créala, agrégala con db.add(categoria)
        #      y usa db.flush() para obtener su id sin hacer commit todavía.
        #   c) Si ya existe un producto con ese sku
        #      (db.query(Producto).filter_by(sku=item["sku"]).first()),
        #      sáltalo con 'continue' para no duplicar.
        #   d) Crea el Producto con los campos del JSON y
        #      categoria_id=categoria.id, y agrégalo con db.add(producto).

        # TODO 3: Confirma todo con db.commit()

        # TODO 4: Imprime cuántos productos se cargaron, por ejemplo:
        #         print(f"Se cargaron {len(datos)} productos.")
        pass
    finally:
        db.close()


if __name__ == "__main__":
    cargar_datos()

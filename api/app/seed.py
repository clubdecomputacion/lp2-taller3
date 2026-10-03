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
        with open(RUTA_PRODUCTOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        cargados = 0

        for item in datos:
            categoria = (
                db.query(Categoria)
                .filter_by(nombre=item["categoria"])
                .first()
            )
            
            if categoria is None:
                categoria = Categoria(nombre=item["categoria"])
                db.add(categoria)
                db.flush()
                
            producto_existente = (
                db.query(Producto)
                .filter_by(sku=item["sku"])
                .first()
            )
            
            if producto_existente is not None:
                continue

            producto = Producto (
                sku=item["sku"],    
                marca=item["marca"],
                nombre=item["nombre"],
                precio=item["precio"],
                foto=item.get("foto"),  
                stock=item["stock"],
                activo=item["activo"],
                categoria_id=categoria.id,
            )
            db.add(producto)
            cargados += 1 

        db.commit()
        print(f"Se cargaron {cargados} productos.")
        
    finally:
        db.close()


if __name__ == "__main__":
    cargar_datos()

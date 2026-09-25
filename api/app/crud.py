"""
Funciones de acceso a datos (Create/Read/Update/Delete).

Separar estas consultas en su propio módulo evita repetir código ORM
dentro de los routers y facilita reutilizarlas o probarlas por separado.
"""

from typing import Optional

from sqlalchemy.orm import Session

from . import models


def obtener_productos(db: Session, categoria_id: Optional[int] = None):
    """Retorna la lista de productos, opcionalmente filtrada por categoría."""
    # TODO 1: construye la consulta base: db.query(models.Producto)
    # TODO 2: si categoria_id no es None, agrega
    #         .filter(models.Producto.categoria_id == categoria_id)
    # TODO 3: retorna el resultado con .all()
    pass


def obtener_producto_por_sku(db: Session, sku: str):
    """Retorna un producto por su SKU, o None si no existe."""
    # TODO 4: db.query(models.Producto).filter(models.Producto.sku == sku).first()
    pass


def obtener_categorias(db: Session):
    """Retorna todas las categorías ordenadas por nombre."""
    # TODO 5: db.query(models.Categoria).order_by(models.Categoria.nombre).all()
    pass

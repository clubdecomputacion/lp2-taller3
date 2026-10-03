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
    query = db.query(models.Producto)
    if categoria_id is not None:
        query = query.filter(models.Producto.categoria_id == categoria_id)
    return query.all()
    


def obtener_producto_por_sku(db: Session, sku: str):
    """Retorna un producto por su SKU, o None si no existe."""
    return db.query(models.Producto).filter(models.Producto.sku == sku).first()


def obtener_categorias(db: Session):
    """Retorna todas las categorías ordenadas por nombre."""
    return db.query(models.Categoria).order_by(models.Categoria.nombre).all()
    

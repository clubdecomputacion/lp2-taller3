"""
Esquemas Pydantic.

Mientras los modelos de models.py describen las TABLAS de la base de
datos, estos esquemas describen la FORMA en que los datos entran y salen
de la API (el "contrato" JSON). FastAPI los usa para:
  - validar automáticamente lo que llega en el body de una petición
  - serializar automáticamente lo que se retorna al cliente
  - generar la documentación interactiva en /docs
"""

from pydantic import BaseModel


class CategoriaBase(BaseModel):
    """Forma de una categoría tal como se expone en la API."""

    id: int

    nombre: str

    class Config:
        # Permite construir este esquema directamente a partir de un
        # objeto SQLAlchemy (Categoria), no solo de un diccionario.
        from_attributes = True


class ProductoBase(BaseModel):
    """Forma de un producto tal como se expone en la API."""

    id: int
    sku: str

   
    marca: str
    nombre: str
    precio: float
    foto: str | None = None
    stock: int
    activo: bool
    disponible: bool         
    categoria: CategoriaBase 
    
    class Config:
        from_attributes = True

"""
Modelos SQLAlchemy (equivalentes a los del Taller 2, pero usando la
sintaxis "clásica" de SQLAlchemy en lugar de Flask-SQLAlchemy, porque
FastAPI no tiene esa extensión).
"""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)

    # TODO 1: Define la columna 'nombre': String(80), nullable=False,
    #         unique=True (igual que en el Taller 2).
    # nombre = Column(...)

    # Relación uno-a-muchos. 'back_populates' exige declarar el lado
    # complementario en el modelo Producto (ver más abajo).
    productos = relationship("Producto", back_populates="categoria")

    def __repr__(self):
        # TODO 2: retorna f"<Categoria {self.nombre}>"
        pass


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)

    # TODO 3: Define las mismas columnas del Taller 2:
    #   sku    -> String(20),  unique=True, nullable=False
    #   marca  -> String(80),  nullable=False
    #   nombre -> String(160), nullable=False
    #   precio -> Float,       nullable=False
    #   foto   -> String(200), nullable=True
    #   stock  -> Integer,     nullable=False, default=0
    #   activo -> Boolean,     nullable=False, default=True
    #
    # sku = Column(...)
    # ...

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    # TODO 4: Define el lado complementario de la relación:
    #   categoria = relationship("Categoria", back_populates="productos")

    def __repr__(self):
        # TODO 5: retorna f"<Producto {self.sku} - {self.nombre}>"
        pass

    @property
    def disponible(self):
        """True si el producto está activo y tiene unidades en stock."""
        # TODO 6: misma lógica del Taller 2 (self.activo and self.stock > 0)
        pass

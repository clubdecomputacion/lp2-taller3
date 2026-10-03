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

    nombre = Column(String(80), nullable=False, unique=True)

    # Relación uno-a-muchos. 'back_populates' exige declarar el lado
    # complementario en el modelo Producto (ver más abajo).
    productos = relationship("Producto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria {self.nombre}>"


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)

    sku = Column(String(20), unique=True, nullable=False)
    marca = Column(String(80), nullable=False)
    nombre = Column(String(160), nullable=False)
    precio = Column(Float, nullable=False)
    foto = Column(String(200), nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    activo = Column(Boolean, nullable=False, default=True)

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="productos")

    def __repr__(self):
        return f"<Producto {self.sku} - {self.nombre}>"

    @property
    def disponible(self):
        """True si el producto está activo y tiene unidades en stock."""
        return self.activo and self.stock > 0

"""
Endpoints relacionados con productos.

Rutas resultantes (por el prefix definido abajo):
    GET /productos/          -> lista todos (o filtrados por categoria_id)
    GET /productos/{sku}     -> detalle de un producto
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[schemas.ProductoBase])
def listar_productos(categoria_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Lista productos. Admite ?categoria_id=<id> como filtro opcional."""
    # TODO 1: llama a crud.obtener_productos(db, categoria_id) y retórnalo
    pass


@router.get("/{sku}", response_model=schemas.ProductoBase)
def obtener_producto(sku: str, db: Session = Depends(get_db)):
    """Retorna un producto por su SKU, o 404 si no existe."""
    # TODO 2: producto = crud.obtener_producto_por_sku(db, sku)
    # TODO 3: si producto es None, lanza:
    #         raise HTTPException(status_code=404, detail="Producto no encontrado")
    # TODO 4: si existe, retórnalo (FastAPI lo serializa con ProductoBase)
    pass

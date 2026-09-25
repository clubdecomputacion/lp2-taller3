"""
Endpoints relacionados con categorías.

Rutas resultantes:
    GET /categorias/   -> lista todas las categorías
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=List[schemas.CategoriaBase])
def listar_categorias(db: Session = Depends(get_db)):
    """Lista todas las categorías registradas."""
    # TODO 1: llama a crud.obtener_categorias(db) y retórnalo
    pass

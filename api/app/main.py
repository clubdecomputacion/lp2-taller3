"""
Punto de entrada de la API (FastAPI).

Se ejecuta con:
    uvicorn app.main:app --host 0.0.0.0 --port 8000
(esto ya lo hace el CMD del Dockerfile).
"""

from fastapi import FastAPI

from .database import Base, engine
from .routers import categorias, productos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tienda Virtual API",
    description="API REST que expone productos y categorías desde PostgreSQL.",
    version="1.0.0",
)


app.include_router(productos.router)
app.include_router(categorias.router)


@app.get("/")
def raiz():
    """Endpoint de salud, útil para confirmar que el servicio está vivo."""
    return {"mensaje": "API de la Tienda Virtual funcionando"}

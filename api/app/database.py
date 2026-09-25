"""
Configuración de la conexión a PostgreSQL con SQLAlchemy "puro"
(sin Flask-SQLAlchemy, porque este servicio ya no es una app Flask).
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# TODO 1: Lee la variable de entorno DATABASE_URL (definida en
#         docker-compose.yml) usando os.environ["DATABASE_URL"]
DATABASE_URL = None

# TODO 2: Crea el engine de SQLAlchemy con create_engine(DATABASE_URL)
engine = None

# TODO 3: Crea la fábrica de sesiones:
#   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = None

# Clase base de la que heredarán todos los modelos (models.py)
Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: entrega una sesión de base de datos y la
    cierra automáticamente al terminar la petición, incluso si hubo error.
    Se usa así en los routers: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

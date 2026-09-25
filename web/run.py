"""
Punto de entrada del frontend.

Ejecutar con:
    python run.py
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # TODO: ejecuta la app escuchando en 0.0.0.0 (no 127.0.0.1) para que
    # sea accesible desde fuera del contenedor, en el puerto 5000.
    # Pista: app.run(host="0.0.0.0", port=5000, debug=True)
    pass

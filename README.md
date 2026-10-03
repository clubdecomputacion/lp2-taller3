# Taller 3 — Tienda Virtual con Docker Compose

Proyecto de Lenguaje de Programación 2. La tienda está dividida en tres
servicios que se comunican por una red privada de Docker Compose:

| Servicio | Tecnología | Responsabilidad |
| --- | --- | --- |
| `web` | Flask | Muestra el catálogo y consulta la API por HTTP. |
| `api` | FastAPI y SQLAlchemy | Expone productos y categorías y consulta la base de datos. |
| `database` | PostgreSQL 15 | Guarda los productos y las categorías. |

El catálogo de ejemplo se encuentra en `api/data/productos.json`. La interfaz
permite filtrar perfumes por casa perfumera y consultar el detalle de cada
producto.

## Requisitos

- Docker y Docker Compose.
- En Windows, Docker Desktop con integración habilitada para la distribución
  Ubuntu de WSL2.
- Terminal abierta en la carpeta del proyecto, donde está `docker-compose.yml`.

Comprueba que Docker está disponible:

```bash
docker --version
docker compose version
```

## Preparar el entorno

Crea el archivo local de variables a partir de la plantilla:

```bash
cp .env.example .env
```

Si quieres, edita `.env` y cambia los valores para tu entorno local. No
compartas este archivo: Git lo ignora. Si cambias el usuario o la contraseña
después de inicializar PostgreSQL, ten en cuenta que el volumen de la base de
datos conserva sus credenciales y datos existentes.

Valida la configuración antes de arrancar:

```bash
docker compose config -q
```

## Iniciar la tienda

Construye las imágenes y arranca los tres servicios:

```bash
docker compose up -d --build
```

Comprueba que están activos:

```bash
docker compose ps
```

La base de datos debe aparecer como `healthy` (o `running`) y los servicios
`api` y `web` como `running`.

Al iniciar, la API crea las tablas. Carga los productos de ejemplo con:

```bash
docker compose exec api python -m app.seed
```

El cargador evita duplicar productos por SKU. Si editas `productos.json` y
agregas referencias nuevas, reconstruye la API y vuelve a ejecutar la semilla:

```bash
docker compose up -d --build api
docker compose exec api python -m app.seed
```

## Abrir y probar

- Tienda: <http://localhost:5000>
- Documentación interactiva de FastAPI: <http://localhost:8000/docs>

En `/docs` puedes probar:

- `GET /productos/`: lista los productos; acepta `categoria_id` como filtro.
- `GET /productos/{sku}`: busca un producto por su SKU.
- `GET /categorias/`: lista las categorías.

Desde la tienda puedes filtrar por categoría y casa perfumera, y abrir el
detalle de un producto. Las imágenes se sirven desde
`web/app/static/images/`; el nombre del archivo debe coincidir con el valor
`foto` del producto en `api/data/productos.json`.

## Comandos útiles

```bash
docker compose ps                 # Ver el estado de los servicios
docker compose logs -f api        # Seguir los registros de la API
docker compose logs -f web        # Seguir los registros de la tienda
docker compose stop               # Detener los servicios sin borrarlos
docker compose start              # Volver a iniciar los servicios
docker compose down               # Detener y quitar contenedores y red
```

`docker compose down` conserva los datos del volumen de PostgreSQL.
`docker compose down -v` también borra ese volumen y los datos guardados;
úsalo solo si realmente quieres reiniciar la base de datos desde cero.

## Cómo se comunican los servicios

Dentro de la red privada de Compose, la API se conecta a PostgreSQL mediante
el nombre de servicio `database`, y Flask llama a la API mediante `api`.
Dentro de un contenedor, `localhost` apunta al propio contenedor, no a los
otros servicios. Los puertos publicados permiten acceder desde el navegador:
`5000` para la tienda y `8000` para la API.

Para conocer los pasos y conceptos del taller, consulta
[docs/GUIA.md](docs/GUIA.md).

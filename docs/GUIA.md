# Taller 3 — Tienda Virtual con Contenedores

## Objetivo

Separar la Tienda Virtual del **Taller 2** en tres contenedores independientes, orquestados con **Docker Compose**:

| Contenedor | Tecnología | Responsabilidad |
|------------|----------------------|-----------------------------------------------------------|
| `web` | Flask | Frontend. Renderiza HTML y solo hace peticiones HTTP a `api`. No conoce la base de datos. |
| `api` | FastAPI + SQLAlchemy | Lógica de negocio y acceso a datos. Expone un API REST. |
| `database` | PostgreSQL 15 | Persistencia de los datos. |

Al terminar sabrás:

- Qué es un contenedor y en qué se diferencia de una máquina virtual.
- Escribir un `Dockerfile` para una app Python.
- Orquestar varios servicios con `docker-compose.yml`.
- Cómo se comunican los contenedores entre sí (red interna, DNS por nombre
  de servicio) y con el exterior (mapeo de puertos).
- Construir una API REST con FastAPI y consumirla desde otra aplicación.
- Usar variables de entorno y un archivo `.env` para no exponer credenciales.

---

## ¿Por qué separar en 3 contenedores?

En los talleres anteriores, una sola aplicación Flask hacía **todo**: mostraba HTML, leía el JSON/la base de datos, aplicaba la lógica de negocio. Eso funciona para un proyecto pequeño, pero tiene límites:

- No puedes escalar el frontend y el backend por separado (por ejemplo, tener 3 réplicas de la API bajo mucha carga y solo 1 del frontend).
- No puedes reemplazar o actualizar una pieza sin tocar las demás (mañana el frontend podría ser una app React, y la API seguiría funcionando igual).
- Un solo proceso mezcla responsabilidades: presentación, lógica de negocio y persistencia.

Separando en contenedores, cada pieza:
- Se desarrolla, prueba y despliega de forma independiente.
- Tiene su propio conjunto de dependencias (Flask no necesita saber que existe PostgreSQL; el `api` no necesita Jinja2).
- Se comunica con las demás por una interfaz bien definida: HTTP/JSON.

Esta forma de dividir una aplicación en servicios pequeños e independientes que se comunican por red es la base de las **arquitecturas de microservicios**.

---

## Requisitos previos

- Haber completado el Taller 2 (o entender su código).
- **Docker** y **Docker Compose** instalados y funcionando en tu Ubuntu/WSL2. Verifica con:

  ```bash
  docker --version
  docker compose version
  ```

  > Si usas Windows con WSL2, la forma recomendada es instalar **Docker Desktop** y habilitar la integración con tu distribución de WSL2 (Settings → Resources → WSL Integration). Así el comando `docker` queda disponible directamente en tu terminal de Ubuntu.

- Conocimientos del Taller 2: qué es un ORM, modelos, relaciones.
- Nociones de HTTP: verbos (GET), códigos de estado (200, 404), JSON.

---

## Conceptos clave antes de empezar

**Imagen vs. contenedor:** una *imagen* es una plantilla inmutable (código + dependencias + sistema operativo base); un *contenedor* es una instancia en ejecución de esa imagen. El `Dockerfile` describe cómo construir la imagen.

**Red interna de Docker Compose:** al ejecutar `docker compose up`, Compose crea automáticamente una red privada donde cada servicio es alcanzable usando **su nombre** como si fuera un hostname. Por eso, dentro de este proyecto, la API se conecta a la base de datos usando el host `database` (no `localhost`, no una IP), y el frontend llama a la API usando el host `api`. `localhost` dentro de un contenedor se refiere al contenedor mismo, nunca a otro contenedor.

**Mapeo de puertos (`ports`):** conecta un puerto de tu máquina (el host) con un puerto del contenedor. Es lo único que necesitas para acceder desde tu navegador; los contenedores entre sí NO usan estos puertos publicados, usan directamente el puerto interno a través de la red de Compose.

**Variables de entorno y `.env`:** en vez de escribir contraseñas o URLs directamente en el código, se inyectan como variables de entorno al arrancar el contenedor. Docker Compose lee automáticamente un archivo llamado `.env` en la raíz del proyecto y sustituye los `${VARIABLE}` que encuentre en `docker-compose.yml`.

---

## Lista de tareas del taller

1. Revisar la estructura del proyecto (`web/`, `api/`, `database` es solo configuración, no tiene carpeta propia porque usamos la imagen oficial).
2. Configurar las variables de entorno (`.env`).
3. Completar el servicio `api`: conexión a PostgreSQL, modelos, esquemas, CRUD, routers y arranque de FastAPI.
4. Completar el servicio `web`: cliente HTTP hacia la API y rutas Flask.
5. Completar `docker-compose.yml` (las conexiones entre servicios).
6. Construir las imágenes y levantar los tres contenedores.
7. Crear las tablas y cargar los datos de prueba dentro del contenedor `api`.
8. Probar la API directamente (documentación interactiva de FastAPI).
9. Probar el frontend de extremo a extremo.
10. Comandos útiles de Docker Compose para el día a día.

---

## Paso 1 — Estructura del proyecto

```
lp2-taller3/
├── docker-compose.yml           # Orquesta los 3 servicios 
├── .env.example                 # Plantilla de variables de entorno
├── .env                         # (lo creas tú, no se versiona)
├── docs/
│   └── GUIA.md
│
├── web/                         # Servicio "web" (Flask, frontend)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── config.py
│   ├── run.py
│   └── app/
│       ├── __init__.py
│       ├── routes.py
│       ├── api_client.py        # Único lugar que sabe hablar HTTP con la API
│       ├── static/
│       │   ├── css/style.css
│       │   └── images/
│       └── templates/
│           ├── base.html
│           ├── index.html
│           ├── detalle.html
│           └── categorias.html
│
└── api/                         # Servicio "api" (FastAPI, backend)
    ├── Dockerfile
    ├── requirements.txt
    ├── data/
    │   └── productos.json       # Semilla de datos (igual rol que en el Taller 2)
    └── app/
        ├── __init__.py
        ├── main.py              # Arranque de FastAPI + registro de routers
        ├── database.py          # engine, SessionLocal, Base, get_db
        ├── models.py            # Categoria, Producto (SQLAlchemy)
        ├── schemas.py           # Esquemas Pydantic (contrato JSON)
        ├── crud.py              # Consultas a la base de datos
        ├── seed.py              # Script de carga inicial
        └── routers/
            ├── __init__.py
            ├── productos.py
            └── categorias.py
```

> Fíjate que `database` (PostgreSQL) **no tiene carpeta propia**: usamos directamente la imagen oficial `postgres:15` desde Docker Hub, sin necesidad de escribir un Dockerfile.

---

## Paso 2 — Variables de entorno

Copia la plantilla y ajusta los valores:

```bash
cp .env.example .env
```

```dotenv
POSTGRES_USER=tienda_user
POSTGRES_PASSWORD=cambia_esta_clave
POSTGRES_DB=tienda_db
SECRET_KEY=cambia-esta-clave-tambien
```

El archivo `.env` está en `.gitignore`: nunca subas contraseñas reales a
un repositorio.

---

## Paso 3 — Completar el servicio `api`

### 3.1 `api/app/database.py`

Debe:
- Leer `DATABASE_URL` desde las variables de entorno con `os.environ`.
- Crear el `engine` con `create_engine(DATABASE_URL)`.
- Crear `SessionLocal` con `sessionmaker(...)`.
- La función `get_db()` ya está completa: es la *dependencia* que FastAPI inyectará en cada endpoint para entregarle una sesión de base de datos.

### 3.2 `api/app/models.py`

Son los mismos modelos `Categoria` y `Producto` del Taller 2, pero con sintaxis SQLAlchemy "pura" (sin `db.Model`, sin `Flask-SQLAlchemy`): heredan de `Base` (definida en `database.py`) y usan `relationship(..., back_populates=...)` en **ambos** lados de la relación, en vez del `backref` de un solo lado que usaste antes. Completa las columnas según los comentarios `# TODO`.

### 3.3 `api/app/schemas.py`

Aquí aparece un concepto nuevo: **el modelo SQLAlchemy y el esquema Pydantic no son lo mismo**, aunque se parezcan.

- El **modelo** (`models.py`) describe la tabla en la base de datos.
- El **esquema** (`schemas.py`) describe cómo se ve ese dato *en la API* (el JSON que viaja por HTTP).

Completa `ProductoBase` agregando los campos que faltan. Fíjate que `categoria` se declara como `CategoriaBase` (el esquema anidado), no como `categoria_id`: así, cuando el frontend reciba un producto, ya viene con el nombre de la categoría incluido, sin tener que hacer una segunda consulta.

### 3.4 `api/app/crud.py`

Estas funciones son casi idénticas a las consultas ORM del Taller 2, solo que ahora reciben explícitamente la sesión `db` como parámetro (en Flask, `Producto.query` la tomaba "mágicamente" del contexto de la petición; aquí se pasa de forma explícita).

### 3.5 `api/app/routers/`

Un *router* de FastAPI agrupa endpoints relacionados, algo similar a un Blueprint de Flask. Completa:
- `productos.py`: `GET /productos/` (con filtro opcional `categoria_id`) y `GET /productos/{sku}`.
- `categorias.py`: `GET /categorias/`.

Fíjate en el parámetro `response_model`: le dice a FastAPI qué esquema usar para validar y documentar la respuesta. Si tu función retorna un objeto `Producto` de SQLAlchemy, FastAPI lo convierte automáticamente al JSON definido por `ProductoBase` (gracias a `from_attributes = True`).

### 3.6 `api/app/main.py`

Debe:
- Crear las tablas en la base de datos al arrancar (`Base.metadata.create_all(bind=engine)`).
- Registrar los dos routers con `app.include_router(...)`.

### 3.7 `api/app/seed.py`

Script para cargar `productos.json` a la base de datos, con la misma lógica del Taller 2 (buscar/crear categoría, evitar duplicados por SKU, un solo `commit()` al final). Se ejecuta manualmente dentro del contenedor (ver Paso 7).

---

## Paso 4 — Completar el servicio `web`

### 4.1 `web/config.py`

Debe leer dos variables de entorno: `SECRET_KEY` y `API_URL` (esta última apuntará a `http://api:8000` dentro de Docker).

### 4.2 `web/app/api_client.py`

Este archivo reemplaza por completo al ORM del Taller 2. En vez de `Producto.query.all()`, ahora hacemos `requests.get(...)` contra la API. Completa las tres funciones (`obtener_productos`, `obtener_producto`, `obtener_categorias`) siguiendo los `# TODO`. Presta atención al manejo de errores: si la API no responde o devuelve un error, estas funciones deben devolver `[]` o `None` en vez de dejar que la excepción rompa la página.

### 4.3 `web/app/routes.py`

Las vistas ahora llaman a `api_client` en vez de a modelos ORM. La estructura de las rutas (`/`, `/producto/<sku>`, `/categorias`) es idéntica a la del Taller 2; lo que cambia es **de dónde vienen los datos**.

### 4.4 Plantillas

Buena noticia: en Jinja2, `producto.nombre` funciona igual sobre un diccionario (lo que ahora llega desde la API) que sobre un objeto ORM (lo que llegaba en el Taller 2). Por eso las plantillas necesitan pocos ajustes; complétalas siguiendo los `# TODO`, y ten en cuenta que `categoria.productos|length` **ya no está disponible** en `categorias.html` (esa relación vivía en el ORM local del Taller 2, no en un diccionario JSON) — queda anotado como reto opcional al final.

---

## Paso 5 — Completar `docker-compose.yml`

Repasa los `# TODO` del archivo:

1. El `healthcheck` de `database`, para que `api` espere a que Postgres esté realmente listo (no solo "arrancado", sino aceptando conexiones).
2. La variable `DATABASE_URL` de `api`, con el formato `postgresql://usuario:password@host:puerto/basededatos`.
3. La variable `API_URL` de `web`, apuntando al servicio `api` (no a `localhost`).
4. El `depends_on` de `web` hacia `api`.

---

## Paso 6 — Construir y levantar los contenedores

Desde la raíz del proyecto (donde está `docker-compose.yml`):

```bash
docker compose up --build
```

- `--build` fuerza a reconstruir las imágenes (necesario la primera vez y cada vez que cambies un `Dockerfile` o `requirements.txt`).
- Verás en la terminal los logs de los tres contenedores entremezclados, cada uno con un color distinto.
- Para dejarlo corriendo en segundo plano: `docker compose up -d --build`.

Verifica que los tres estén corriendo:

```bash
docker compose ps
```

Deberías ver `lp2taller3-database`, `lp2taller3-api` y `lp2taller3-web` con estado `running` (o `healthy` para la base de datos).

---

## Paso 7 — Crear tablas y cargar datos de prueba

Las tablas se crean automáticamente cuando arranca `api` (por el `Base.metadata.create_all()` del Paso 3.6). Pero los datos de ejemplo hay que cargarlos manualmente, ejecutando el script **dentro** del contenedor:

```bash
docker compose exec api python -m app.seed
```

`docker compose exec` ejecuta un comando dentro de un contenedor que ya está corriendo — es el equivalente a "entrar" al contenedor y correr algo ahí, sin necesidad de instalar nada en tu máquina anfitriona.

Para confirmar que los datos quedaron en Postgres, puedes entrar al cliente `psql` dentro del propio contenedor de la base de datos:

```bash
docker compose exec database psql -U tienda_user -d tienda_db -c "SELECT sku, nombre FROM productos;"
```

(ajusta el usuario/base de datos si cambiaste los valores del `.env`)

---

## Paso 8 — Probar la API directamente

FastAPI genera documentación interactiva automáticamente. Con los contenedores corriendo, abre en tu navegador:

```
http://localhost:8000/docs
```

Ahí puedes ejecutar cada endpoint (`GET /productos/`, `GET /productos/{sku}`, `GET /categorias/`) directamente desde el navegador y ver la respuesta JSON, sin necesidad de Postman ni curl. Es una forma rápida de verificar que tu `api` funciona **antes** de tocar el frontend.

---

## Paso 9 — Probar el frontend

Abre:

```
http://localhost:5000
```

Verifica:
1. El catálogo carga los productos (que en realidad vienen de `api`, que a su vez los trae de `database`: tres saltos de red para pintar una página).
2. El filtro por categoría funciona (`/?categoria=<id>`).
3. El detalle de un producto muestra los datos completos, incluida la categoría.
4. Un SKU inexistente responde 404.
5. Si detienes el contenedor `api` (`docker compose stop api`) y recargas el frontend, `web` no debería explotar con un error 500: gracias al manejo de errores de `api_client.py`, debería mostrar una página vacía o un mensaje controlado. Vuelve a levantar la API con `docker compose start api`.

---

## Paso 10 — Comandos útiles de Docker Compose

| Comando | Qué hace |
|---|---|
| `docker compose up -d --build` | Construye y levanta todo en segundo plano |
| `docker compose ps` | Lista el estado de los servicios |
| `docker compose logs -f api` | Sigue en vivo los logs de un servicio |
| `docker compose exec api bash` | Abre una terminal dentro del contenedor `api` |
| `docker compose restart web` | Reinicia un solo servicio |
| `docker compose stop` | Detiene los contenedores sin borrarlos |
| `docker compose down` | Detiene y elimina los contenedores (los datos del volumen se conservan) |
| `docker compose down -v` | Igual que arriba, pero **también borra los volúmenes** (¡pierdes los datos de Postgres!) |

---

## Errores frecuentes

| Síntoma | Causa probable |
|---|---|
| `api` se reinicia en bucle | La base de datos aún no estaba lista; revisa el `healthcheck` y el `depends_on`. |
| `psycopg2.OperationalError: could not translate host name "database"` | Estás intentando conectarte desde tu máquina anfitriona en vez de desde dentro de la red de Compose; o el servicio no se llama exactamente `database`. |
| El frontend muestra catálogo vacío pero `/docs` de la API sí trae datos | Revisa `API_URL` en `web` — probablemente apunta a `localhost` en vez de `api`. |
| `Bind for 0.0.0.0:5000 failed: port is already allocated` | Ya tienes algo corriendo en ese puerto en tu máquina; cámbialo en `ports` (ej. `"5050:5000"`) o detén el otro proceso. |
| Cambios en el código no se reflejan | Si no usas volúmenes montados, necesitas reconstruir la imagen: `docker compose up --build`. |
| `relation "productos" does not exist` | El `create_all()` no se ejecutó (revisa `main.py`) o estás corriendo `seed.py` contra una base de datos distinta. |

---

## Checklist final

- [ ] `.env` creado a partir de `.env.example`, con valores propios.
- [ ] `api/app/database.py` conecta correctamente a PostgreSQL.
- [ ] Modelos, esquemas, CRUD y routers de la API completos.
- [ ] `GET /docs` muestra la documentación interactiva y los endpoints responden datos reales.
- [ ] `web/app/api_client.py` maneja tanto respuestas exitosas como errores/caídas de la API.
- [ ] El frontend en `http://localhost:5000` muestra el catálogo completo.
- [ ] `docker compose ps` muestra los 3 servicios corriendo.
- [ ] Puedes explicar, en tus propias palabras, por qué `api` se conecta a `database` (y no a `localhost`) y por qué `web` se conecta a `api` (y no directamente a la base de datos).

## Retos adicionales

1. **Volumen para imágenes:** monta `web/app/static/images` como volumen compartido con `api`, o expón las imágenes directamente desde la API, para no duplicar archivos entre los dos servicios.
2. **Conteo de productos por categoría en la API:** agrega un campo `total_productos` al esquema `CategoriaBase`, calculado en `crud.py` con una consulta agregada, para poder mostrarlo en `categorias.html`.
3. **Documentación con ejemplos:** usa el parámetro `examples` de Pydantic para enriquecer la documentación automática de `/docs`.
4. **Reverse proxy:** agrega un cuarto contenedor con **Nginx** que exponga un único puerto al exterior y enrute `/api/*` hacia `api` y el resto hacia `web`.
5. **CI simple:** escribe un script que corra `docker compose up --build -d`, espere a que los servicios estén `healthy` y haga una petición de prueba a `/productos/` para validar el despliegue.


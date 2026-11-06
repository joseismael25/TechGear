# TechGear — API FastAPI + portal Django

> **Corrección incluida:** se corrigió el error que provocaba HTTP 500 al abrir `/dashboard/`. La función auxiliar `_fetch_private_list()` ya no tiene el decorador de vistas `@session_required`; además, el panel tolera campos numéricos incompletos sin detenerse.

Proyecto híbrido de catálogo e inventario. FastAPI expone la API y guarda usuarios, productos y pedidos en MongoDB Atlas. Django sirve las páginas HTML, gestiona la sesión del navegador y consume esa API. SQLite se utiliza únicamente para las tablas internas de Django (sesiones y administración); no reemplaza MongoDB.

## Requisitos

- Python 3.12 o superior (el proyecto está preparado para Django 6.1 y Python 3.14).
- MongoDB Atlas y una URI de conexión válida.
- Dos terminales: una para FastAPI y otra para Django.

## 1. Configurar la API

Si ya tienes los archivos `.env` creados, consérvalos: no los reemplaces al copiar esta versión. Comprueba principalmente que `MONGO_URI` apunte a tu base de datos Atlas y que `ADMIN_EMAILS` contenga el correo con el que te vas a registrar.

En Windows PowerShell:

```powershell
cd techgear_api
py -m venv venv
.\venv\Scripts\Activate.ps1
Copy-Item .env.example .env
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

Abre `techgear_api/.env` y configura:

- `MONGO_URI`: URI de MongoDB Atlas; agrega tu IP en Network Access de Atlas y revisa las credenciales.
- `SECRET_KEY`: clave aleatoria privada de al menos 32 caracteres.
- `ADMIN_EMAILS`: correo que tendrá permisos de administrador. Regístrate en el portal con ese mismo correo.

Inicia la API:

```powershell
py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Documentación interactiva: http://127.0.0.1:8000/docs

## 2. Configurar Django

Abre otra terminal PowerShell en la carpeta principal del proyecto (la que contiene `manage.py`):

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
Copy-Item .\techgear_web\.env.example .\techgear_web\.env
py -m pip install --upgrade pip
py -m pip install -r .\techgear_web\requirements.txt
```

Abre `techgear_web/.env` y confirma que `API_URL=http://127.0.0.1:8000`. Cambia `DJANGO_SECRET_KEY` por una clave privada propia. Para desarrollo local deja `DJANGO_DEBUG=True`.

Ejecuta las migraciones y el servidor desde esa misma carpeta principal:

```powershell
py manage.py check
py manage.py findstatic store/css/styles.css --verbosity 2
py manage.py migrate
py manage.py runserver 127.0.0.1:8001
```

Abre http://127.0.0.1:8001

## 3. Crear cuenta administradora

1. Agrega tu correo en `ADMIN_EMAILS` dentro de `techgear_api/.env`.
2. Reinicia FastAPI si ya estaba ejecutándose.
3. En el portal Django selecciona **Registrarse** y crea una cuenta con ese correo.
4. Si esa cuenta ya existía antes de agregar el correo a `ADMIN_EMAILS`, cierra sesión e inicia sesión de nuevo: la API actualiza su rol a `admin` al autenticarla.
5. Inicia sesión. La API asigna el rol `admin` desde el servidor; no se puede elegir desde el formulario.

Los demás correos se registran como clientes. Ambos roles pueden entrar a **Mi panel**; solo el administrador puede crear, editar o eliminar productos.

## 4. Estructura

- `techgear_api/`: API FastAPI, esquemas Pydantic, autenticación JWT y acceso MongoDB.
- `techgear_web/`: proyecto Django, aplicación `store`, templates y archivos estáticos. También se incluye un `manage.py` en la carpeta principal para ejecutar los comandos sin entrar a esta subcarpeta.
- `techgear_web/db.sqlite3`: se genera localmente al ejecutar `py manage.py migrate`; no es la base de productos, que está en MongoDB Atlas.

## Notas importantes

- Ejecuta los dos servidores al mismo tiempo. Si Django indica que no puede conectar con la API, comprueba que FastAPI esté activo y que `API_URL` sea correcto.
- No subas los archivos `.env` a Git ni compartas sus claves.
- El dashboard presenta métricas reales derivadas de los productos y pedidos de la API.
- El catálogo incluye carrito persistente en `localStorage`. Para finalizar una compra el cliente debe iniciar sesión; Django envía el pedido a FastAPI y la API verifica el precio vigente y descuenta el stock antes de registrar el pedido. Es un flujo de demostración: no integra una pasarela bancaria ni procesa pagos reales.
- El modelo actual no contiene campos de calificación, reseñas ni precio anterior; por eso el catálogo muestra “Sin reseñas” y no inventa descuentos. Esos elementos solo pueden mostrarse como datos reales cuando se incorporen a los productos.
- Para producción configura HTTPS, `DJANGO_DEBUG=False`, hosts permitidos, cookies seguras, secretos reales y un servidor ASGI/WSGI de producción. `runserver` es solo para desarrollo.
- Lighthouse depende también del navegador, red, servidor y contenido cargado. Se aplicaron mejoras de accesibilidad, semántica, metadatos y carga ligera, pero no se puede prometer una puntuación fija de 100 sin medir el despliegue real.

## 5. Imágenes de productos (archivo o enlace)

Desde el portal inicia sesión con una cuenta administradora y abre **Mi panel → Nuevo producto** o edita un producto existente. En el formulario puedes:

- Seleccionar una imagen JPG, PNG o WebP desde tu computador (máximo 5 MB). Django la envía a FastAPI y FastAPI la guarda en la colección `product_images` de MongoDB.
- O pegar una URL pública que empiece por `https://` o `http://`.
- Ver una vista previa antes de guardar y reemplazar o quitar la imagen al editar.

Las imágenes cargadas desde el computador se sirven mediante `GET /images/{id}`. Configura `PUBLIC_API_URL` en `techgear_api/.env` con la dirección donde los navegadores podrán acceder a FastAPI. Para desarrollo local usa `PUBLIC_API_URL=http://127.0.0.1:8000`. En producción debe ser la URL HTTPS pública de la API.

Instala las nuevas dependencias de FastAPI ejecutando nuevamente `py -m pip install -r requirements.txt` dentro de su entorno virtual.


## Corrección adicional de archivos CSS

Los archivos estáticos están disponibles en dos ubicaciones para que Django pueda encontrarlos:
- `techgear_web/static/store/` (carpeta estática general del proyecto).
- `techgear_web/store/static/store/` (carpeta estática propia de la aplicación).

En desarrollo (`DJANGO_DEBUG=True`), las rutas `/static/` también se sirven explícitamente desde `techgear_web/static/`.
Ejecuta los comandos desde la carpeta principal que contiene este `README.md` y el `manage.py`:
```powershell
py manage.py findstatic store/css/styles.css --verbosity 2
py manage.py runserver 127.0.0.1:8001
```


## 6. Catálogo, carrito y pedidos

- El botón **Agregar al carrito** valida la cantidad frente al stock conocido y actualiza el contador de la burbuja flotante fija.
- El carrito se conserva en el navegador mediante `localStorage`; permite cambiar cantidades, recalcular subtotales y total, eliminar productos y vaciarlo; los campos de precio heredados se normalizan al leer el almacenamiento.
- Para finalizar el pedido debes iniciar sesión. Django envía los artículos a `POST /checkout/` y FastAPI crea el pedido en `POST /orders`.
- FastAPI vuelve a consultar el precio en MongoDB y descuenta el inventario con una actualización condicionada al stock disponible. El precio que llegue desde el navegador no se usa para calcular el total.
- El flujo registra pedidos y actualiza existencias, pero **no cobra dinero**: no hay pasarela de pagos conectada.
- El catálogo actual no tiene columnas de reseñas/calificación ni precio anterior. La interfaz lo indica como “Sin reseñas” y no muestra descuentos inventados.

## Ajustes de carrito e informe de compra

La versión corregida conserva `techgear_cart_v1` en `localStorage` y normaliza los campos de precio (`price`, `precio`, `valor` y `precio_unitario`) al leer datos antiguos. Los importes se muestran y calculan en COP usando el precio validado por FastAPI al crear el pedido. El carrito ahora se abre desde una burbuja fija en la esquina inferior derecha; el catálogo mantiene tarjetas con texto de alto contraste. Al completar el pedido se presenta un informe imprimible con los datos devueltos por la API. El historial de pedidos continúa guardándose en la colección `orders` de MongoDB y aparece en el panel según el rol del usuario. No se conecta ninguna pasarela ni se realiza un cobro real.

### Arranque local (Windows PowerShell)

1. **Primero inicia FastAPI**, desde `techgear_api` y con su entorno virtual activo:
   ```powershell
   py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
2. **Después inicia Django**, desde la carpeta raíz del proyecto y en otra terminal con el entorno virtual de Django activo:
   ```powershell
   py manage.py migrate
   py manage.py runserver 127.0.0.1:8001
   ```
3. Abre `http://127.0.0.1:8001`. La API debe permanecer ejecutándose en la primera terminal.

> Para verificar Django localmente instala primero las dependencias de `techgear_web/requirements.txt` en el entorno virtual de Django. La comprobación automática `manage.py check` no pudo ejecutarse en este entorno de edición porque Django no está instalado aquí.


## Actualización visual del inventario después de comprar

FastAPI descuenta las unidades de `products.stock` en MongoDB al registrar el pedido. Después de cerrar el informe de compra, el navegador limpia el carrito y recarga el catálogo; así Django vuelve a consultar `GET /products` y muestra las existencias actualizadas. El panel también consulta nuevamente los productos al abrirlo.

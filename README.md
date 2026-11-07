💻 TechGear – Sistema de Gestión de Productos Tecnológicos

TechGear es una aplicación web orientada a la gestión y comercialización de productos tecnológicos. El proyecto integra una API REST desarrollada con FastAPI, una interfaz web desarrollada con Django y una base de datos MongoDB Atlas.

El sistema permite consultar productos, administrar inventario, gestionar usuarios, agregar productos al carrito y registrar pedidos.

---

🌐 Enlaces del proyecto

Servicio| Plataforma| Enlace
API REST – FastAPI| Render| https://techgear-yxm3.onrender.com
Documentación API| Render / Swagger| https://techgear-yxm3.onrender.com/docs
Productos API| Render| https://techgear-yxm3.onrender.com/products
Página web – Django| Vercel| https://tech-gear-kappa.vercel.app/
Base de datos| MongoDB Atlas| https://cloud.mongodb.com/

---

🛠️ Tecnologías utilizadas

Backend – API

- Python
- FastAPI
- Uvicorn
- Pydantic
- Motor
- PyMongo
- JWT para autenticación
- Pillow para procesamiento de imágenes

Frontend – Aplicación web

- Django
- HTML5
- CSS3
- JavaScript
- Requests

Base de datos

- MongoDB Atlas: almacenamiento de productos, usuarios, pedidos e imágenes.
- SQLite: almacenamiento local de las tablas internas de Django, como sesiones y administración.

Servicios de despliegue

- Render: alojamiento de la API FastAPI.
- Vercel: alojamiento de la aplicación web Django.
- GitHub: control de versiones y almacenamiento del código fuente.

---

⚙️ Arquitectura del proyecto

El proyecto está dividido en tres componentes principales:

1. FastAPI: procesa las solicitudes, administra los productos, usuarios y pedidos.
2. Django: proporciona la interfaz gráfica y consume los servicios de la API.
3. MongoDB Atlas: almacena la información principal del sistema.

Flujo de comunicación

             USUARIO
                |
                v
       DJANGO - VERCEL
                |
                | Solicitudes HTTP
                v
       FASTAPI - RENDER
                |
                | Consultas y operaciones
                v
          MONGODB ATLAS

Django consume la API utilizando la variable de entorno "API_URL".

---

📁 Estructura del proyecto

TechGear_E_F/
│
├── README.md
├── .gitignore
├── manage.py
│
├── techgear_api/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   │
│   ├── db/
│   │   └── database.py
│   │
│   └── models/
│       └── schemas.py
│
└── techgear_web/
    ├── manage.py
    ├── requirements.txt
    ├── .env
    ├── db.sqlite3
    │
    ├── techgear_web/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    └── store/
        ├── views.py
        ├── urls.py
        ├── models.py
        ├── admin.py
        ├── templates/
        └── static/

---

🚀 Instalación y ejecución local

Requisitos

- Python 3.12 o superior.
- Visual Studio Code.
- MongoDB Atlas.
- Git.
- Conexión a Internet.

1. Descargar el proyecto

Clonar el repositorio:

git clone https://github.com/joseismael25/TechGear.git

Entrar a la carpeta:

cd TechGear

2. Configurar FastAPI

Desde la carpeta principal:

cd techgear_api

Crear entorno virtual:

py -m venv venv

Activar el entorno virtual en Windows:

.\venv\Scripts\Activate.ps1

Instalar dependencias:

py -m pip install -r requirements.txt

Crear o configurar el archivo ".env" dentro de "techgear_api":

MONGO_URI=TU_URI_DE_MONGODB_ATLAS
SECRET_KEY=TU_CLAVE_SECRETA
ADMIN_EMAILS=tu_correo@ejemplo.com
PUBLIC_API_URL=http://127.0.0.1:8000

Iniciar FastAPI:

py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

Documentación local:

http://127.0.0.1:8000/docs

3. Configurar Django

Abrir una segunda terminal y regresar a la carpeta principal del proyecto.

Crear entorno virtual:

py -m venv venv

Activar el entorno:

.\venv\Scripts\Activate.ps1

Instalar dependencias:

py -m pip install -r techgear_web/requirements.txt

Crear o configurar el archivo ".env" dentro de "techgear_web":

API_URL=http://127.0.0.1:8000
DJANGO_SECRET_KEY=TU_CLAVE_SECRETA
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

Ejecutar las migraciones:

py manage.py migrate

Iniciar Django:

py manage.py runserver 127.0.0.1:8001

Abrir en el navegador:

http://127.0.0.1:8001

Importante: FastAPI debe permanecer ejecutándose en la primera terminal mientras se utiliza Django.

---

☁️ Configuración del despliegue

FastAPI – Render

Dirección pública:

https://techgear-yxm3.onrender.com

En Render, dentro de Environment Variables, se configuran las siguientes variables:

Variable| Descripción
"MONGO_URI"| Conexión a MongoDB Atlas
"SECRET_KEY"| Clave privada para autenticación
"ADMIN_EMAILS"| Correos autorizados como administradores
"PUBLIC_API_URL"| URL pública de FastAPI para las imágenes

"PUBLIC_API_URL" debe contener:

https://techgear-yxm3.onrender.com

Django – Vercel

Dirección pública:

https://tech-gear-kappa.vercel.app/

En las variables de entorno de Vercel se configura:

Variable| Descripción
"API_URL"| Dirección pública de FastAPI
"DJANGO_SECRET_KEY"| Clave privada de Django
"DJANGO_ALLOWED_HOSTS"| Dominios autorizados
"DJANGO_DEBUG"| Modo de depuración

La variable "API_URL" debe contener:

https://techgear-yxm3.onrender.com

Para producción se recomienda:

DJANGO_DEBUG=False

Nota: Las variables privadas se configuran directamente en los paneles de Render y Vercel. Los archivos ".env" no deben subirse a GitHub.

---

🛍️ Funcionalidades principales

Catálogo de productos

- Visualización de productos tecnológicos.
- Consulta de información y precios.
- Consulta de disponibilidad y existencias.
- Visualización de imágenes.

Gestión de usuarios

- Registro de usuarios.
- Inicio y cierre de sesión.
- Autenticación mediante JWT.
- Roles de administrador y cliente.

Administración

- Crear productos.
- Editar productos.
- Eliminar productos.
- Consultar inventario.
- Consultar estadísticas y pedidos.

Carrito de compras

- Agregar productos al carrito.
- Modificar cantidades.
- Eliminar productos.
- Calcular subtotales y total.
- Persistencia mediante "localStorage".

Pedidos

- Registro de pedidos.
- Validación de precios desde la API.
- Descuento de existencias.
- Historial de pedidos.
- Informe imprimible de compra.

Importante: El sistema registra pedidos y actualiza inventario, pero no tiene integrada una pasarela de pagos ni realiza cobros reales.

Imágenes

- Carga de imágenes JPG, PNG y WebP.
- Tamaño máximo de 5 MB.
- Almacenamiento de imágenes en MongoDB.
- Posibilidad de utilizar enlaces públicos de imágenes.

---

🔐 Seguridad

- Las contraseñas de los usuarios se almacenan mediante hash.
- Se utiliza autenticación JWT.
- Los permisos administrativos son controlados desde la API.
- Las claves privadas se gestionan mediante variables de entorno.
- Los archivos ".env" están excluidos del repositorio mediante ".gitignore".

Nunca publiques contraseñas, tokens, URI de MongoDB ni claves privadas.

---

---

👨‍💻 Autor

Proyecto: TechGear

Tecnologías principales: Python, FastAPI, Django, JavaScript y MongoDB Atlas.

Repositorio: https://github.com/joseismael25/TechGear

Despliegue: Render y Vercel.

---

📌 Observaciones finales

TechGear es un proyecto de gestión de productos tecnológicos que integra servicios independientes mediante una API REST.

Su arquitectura permite separar la lógica del backend, la interfaz web y el almacenamiento de datos, facilitando el mantenimiento y la evolución del sistema.
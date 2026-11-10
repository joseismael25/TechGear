<div align="center">TECHGEAR

Plataforma web de gestión y comercialización de productos tecnológicos

Una solución que integra una aplicación web, una API REST y una base de datos en la nube.

"Aplicación web" (https://tech-gear-kappa.vercel.app/) · "API REST" (https://techgear-yxm3.onrender.com) · "Documentación API" (https://techgear-yxm3.onrender.com/docs)

"Python" (https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
"Django" (https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
"FastAPI" (https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
"MongoDB" (https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
"JavaScript" (https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

</div>---

1. ¿Qué es TechGear?

TechGear es una plataforma web diseñada para facilitar la consulta y administración de productos tecnológicos.

El proyecto permite visualizar un catálogo de productos, gestionar usuarios, administrar el inventario y registrar pedidos desde una aplicación web.

Su desarrollo utiliza una arquitectura dividida en dos partes principales:

- Django: se encarga de la interfaz web y de la interacción con el usuario.
- FastAPI: procesa las solicitudes, administra las operaciones y se comunica con MongoDB Atlas.

De esta manera, ambos componentes trabajan juntos para ofrecer una aplicación organizada y funcional.

2. ¿Cómo funciona el sistema?

TechGear utiliza tres componentes principales:

Componente| Función
Django| Muestra la página web y gestiona la navegación del usuario.
FastAPI| Procesa las solicitudes y ejecuta las operaciones del sistema.
MongoDB Atlas| Almacena la información principal de usuarios, productos y pedidos.

Arquitectura del proyecto

             USUARIO
                |
                v
        APLICACIÓN WEB
             DJANGO
             VERCEL
                |
                | Solicitudes HTTP
                v
            API REST
             FASTAPI
             RENDER
                |
                | Consulta y almacenamiento
                v
          MONGODB ATLAS

En pocas palabras: el usuario interactúa con Django, Django se comunica con FastAPI y FastAPI consulta o actualiza la información en MongoDB Atlas.

3. Funcionalidades principales

🛍️ Productos

- Visualización del catálogo de productos.
- Consulta de información y detalles.
- Registro de nuevos productos.
- Actualización de información.
- Eliminación de productos.

👤 Usuarios

- Registro de usuarios.
- Inicio de sesión.
- Consulta del perfil.
- Autenticación mediante tokens JWT.
- Diferenciación de roles de usuario.

📦 Pedidos

- Registro de pedidos.
- Consulta de pedidos.
- Gestión de información relacionada con las compras.

🖼️ Imágenes

- Carga de imágenes de productos.
- Consulta de imágenes mediante la API.

🔐 Seguridad

- Autenticación mediante JWT.
- Protección de operaciones que requieren autorización.
- Configuración de variables de entorno.
- Control de acceso según los permisos establecidos.

4. Tecnologías utilizadas

Las siguientes herramientas se utilizaron durante el desarrollo:

Tecnología| Uso dentro del proyecto
Python| Lenguaje principal del backend.
Django| Desarrollo de la aplicación web.
FastAPI| Creación de la API REST.
MongoDB Atlas| Base de datos NoSQL en la nube.
Motor / PyMongo| Conexión y operaciones con MongoDB.
HTML5| Estructura de las páginas.
CSS3| Diseño y estilos visuales.
JavaScript| Interactividad de la interfaz.
JWT| Autenticación y autorización.
Pillow| Procesamiento de imágenes.
Git y GitHub| Control de versiones y almacenamiento del código.
Render| Despliegue de la API.
Vercel| Despliegue de la aplicación web.

5. Estructura del proyecto

El proyecto está dividido en dos módulos principales:

TechGear/
│
├── techgear_api/
│   ├── main.py
│   ├── requirements.txt
│   │
│   ├── db/
│   │   └── database.py
│   │
│   └── models/
│       └── schemas.py
│
├── techgear_web/
│   ├── manage.py
│   ├── requirements.txt
│   │
│   ├── techgear_web/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── store/
│       ├── views.py
│       ├── urls.py
│       ├── models.py
│       ├── admin.py
│       ├── templates/
│       └── static/
│
├── .gitignore
└── README.md

¿Qué contiene cada módulo?

"techgear_api/"

Contiene el backend del proyecto.

- "main.py": define la API y sus endpoints.
- "db/database.py": configura la conexión con MongoDB Atlas.
- "models/schemas.py": contiene los esquemas para validar la información.
- "requirements.txt": contiene las dependencias de FastAPI.

"techgear_web/"

Contiene la aplicación desarrollada con Django.

- "settings.py": configuración general del proyecto.
- "urls.py": rutas principales.
- "views.py": lógica de las vistas.
- "templates/": archivos HTML.
- "static/": archivos CSS, JavaScript e imágenes.
- "requirements.txt": dependencias de Django.

6. Instalación y ejecución

Para ejecutar TechGear localmente necesitas tener instalado Python y Git.

Paso 1. Descargar el proyecto

Clona el repositorio:

git clone https://github.com/joseismael25/TechGear.git

Entra en la carpeta del proyecto:

cd TechGear

Paso 2. Ejecutar FastAPI

Abre una terminal y entra en la carpeta de la API:

cd techgear_api

Crea un entorno virtual:

python -m venv venv

Actívalo en Windows:

.\venv\Scripts\Activate.ps1

Instala las dependencias:

pip install -r requirements.txt

Crea el archivo ".env" dentro de "techgear_api/":

MONGO_URI=TU_URI_DE_MONGODB
SECRET_KEY=TU_CLAVE_SECRETA
ADMIN_EMAILS=correo_admin@ejemplo.com
PUBLIC_API_URL=http://127.0.0.1:8000
CORS_ORIGINS=http://127.0.0.1:8001

Inicia el servidor:

uvicorn main:app --reload

La API estará disponible en:

- API: http://127.0.0.1:8000
- Documentación Swagger: http://127.0.0.1:8000/docs
- Documentación ReDoc: http://127.0.0.1:8000/redoc

Paso 3. Ejecutar Django

Abre una segunda terminal y entra en la carpeta principal de Django:

cd techgear_web

Crea un entorno virtual:

python -m venv venv

Actívalo:

.\venv\Scripts\Activate.ps1

Instala las dependencias:

pip install -r requirements.txt

Crea el archivo ".env" dentro de "techgear_web/":

API_URL=http://127.0.0.1:8000
DJANGO_SECRET_KEY=TU_CLAVE_SECRETA_DJANGO
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_SECURE_COOKIES=False

Ejecuta las migraciones:

python manage.py migrate

Inicia Django:

python manage.py runserver 8001

Abre la aplicación en el navegador:

http://127.0.0.1:8001

«Importante: debes mantener los dos servidores activos. FastAPI procesa las solicitudes del backend y Django muestra la aplicación web.»

7. Variables de entorno

Las variables de entorno permiten configurar las conexiones y proteger información privada.

FastAPI

Variable| Descripción
"MONGO_URI"| Dirección de conexión a MongoDB Atlas.
"SECRET_KEY"| Clave para firmar los tokens JWT.
"ADMIN_EMAILS"| Correos autorizados para el rol administrador.
"PUBLIC_API_URL"| Dirección pública de la API.
"CORS_ORIGINS"| Direcciones autorizadas para consumir la API.

Django

Variable| Descripción
"API_URL"| Dirección de la API FastAPI.
"DJANGO_SECRET_KEY"| Clave secreta de Django.
"DJANGO_DEBUG"| Activa o desactiva el modo de depuración.
"DJANGO_ALLOWED_HOSTS"| Dominios permitidos para acceder a Django.
"DJANGO_SECURE_COOKIES"| Configura el uso de cookies seguras.

Nota de seguridad: los archivos ".env" contienen información privada. No deben subirse a GitHub ni compartirse públicamente.

8. Despliegue del proyecto

TechGear se encuentra publicado utilizando dos plataformas:

Servicio| Plataforma| Dirección
Aplicación web| Vercel| "tech-gear-kappa.vercel.app" (https://tech-gear-kappa.vercel.app/)
API REST| Render| "techgear-yxm3.onrender.com" (https://techgear-yxm3.onrender.com)
Documentación API| Render| "Swagger UI" (https://techgear-yxm3.onrender.com/docs)
Base de datos| MongoDB Atlas| "MongoDB" (https://www.mongodb.com/atlas)

Configuración de producción

- En Render se configuran las variables de entorno de FastAPI.
- En Vercel se configuran las variables de entorno de Django.
- La variable "API_URL" de Django debe apuntar a la dirección pública de FastAPI.
- MongoDB Atlas almacena los datos principales de la aplicación.

9. Endpoints principales de la API

La API cuenta con diferentes rutas para gestionar la información del sistema.

Método| Ruta| Función
POST| "/auth/login"| Iniciar sesión.
POST| "/users"| Registrar usuarios.
GET| "/users/me"| Consultar el perfil.
GET| "/users"| Consultar usuarios.
POST| "/products"| Crear productos.
GET| "/products"| Consultar productos.
GET| "/products/{id}"| Consultar un producto.
PUT| "/products/{id}"| Actualizar productos.
DELETE| "/products/{id}"| Eliminar productos.
POST| "/orders"| Registrar pedidos.
GET| "/orders"| Consultar pedidos.
POST| "/images"| Cargar imágenes.
GET| "/images/{image_id}"| Consultar imágenes.

Para conocer los parámetros, respuestas y requisitos de autenticación de cada endpoint, consulta la documentación:

"Ver documentación interactiva de TechGear API" (https://techgear-yxm3.onrender.com/docs)

10. Información del proyecto

Dato| Información
Nombre| TechGear
Tipo| Aplicación web con API REST
Backend| Python, FastAPI y Django
Base de datos principal| MongoDB Atlas
Repositorio| "GitHub - TechGear" (https://github.com/joseismael25/TechGear)
Despliegue web| Vercel
Despliegue API| Render

---

<div align="center">TECHGEAR

Tecnología, innovación y desarrollo web.

Desarrollado como proyecto de software.

"Visitar aplicación" (https://tech-gear-kappa.vercel.app/) · "Ver código fuente" (https://github.com/joseismael25/TechGear)

</div>
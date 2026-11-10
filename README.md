🚀 TECHGEAR

Plataforma web para la gestión y administración de productos

<p align="center">
  <strong>TechGear</strong> es una aplicación web que integra tecnologías modernas para gestionar productos, usuarios, imágenes y pedidos mediante una arquitectura basada en Django, FastAPI y MongoDB.
</p><p align="center">
  <a href="https://tech-gear-kappa.vercel.app/">Aplicación web</a> ·
  <a href="https://techgear-yxm3.onrender.com/">API REST</a> ·
  <a href="https://techgear-yxm3.onrender.com/docs">Documentación API</a>
</p>---

📌 Tabla de contenido

1. "Descripción del proyecto" (#-descripción-del-proyecto)
2. "Objetivos" (#-objetivos-del-proyecto)
3. "Características principales" (#-características-principales)
4. "Tecnologías utilizadas" (#-tecnologías-utilizadas)
5. "Arquitectura del sistema" (#-arquitectura-del-sistema)
6. "Estructura del proyecto" (#-estructura-del-proyecto)
7. "Instalación y configuración" (#-instalación-y-configuración)
8. "Variables de entorno" (#-variables-de-entorno)
9. "Ejecución del proyecto" (#-ejecución-del-proyecto)
10. "Endpoints de la API" (#-endpoints-de-la-api)
11. "Despliegue" (#-despliegue)
12. "Control de versiones" (#-control-de-versiones)

---

📖 Descripción del proyecto

TechGear es una plataforma web orientada a la gestión de productos y operaciones relacionadas con una tienda de tecnología.

El proyecto está compuesto por dos módulos principales:

- FastAPI: encargado de proporcionar los servicios REST, gestionar las solicitudes y comunicarse con MongoDB.
- Django: encargado de desarrollar la aplicación web, administrar las vistas y ofrecer la interfaz de interacción con el usuario.

Ambos módulos trabajan de manera integrada para ofrecer una aplicación organizada y escalable.

🎯 Objetivos del proyecto

- Desarrollar una aplicación web utilizando tecnologías actuales.
- Implementar una API REST para gestionar la información.
- Integrar una base de datos NoSQL en la nube.
- Implementar mecanismos de autenticación y autorización.
- Organizar el proyecto mediante una arquitectura modular.
- Desplegar la aplicación web y la API en servicios independientes.

⚙️ Características principales

🛍️ Gestión de productos

- Registro de productos.
- Consulta del listado de productos.
- Consulta de productos individuales.
- Actualización de información.
- Eliminación de productos.

👤 Gestión de usuarios

- Registro de usuarios.
- Inicio de sesión.
- Consulta de información del usuario autenticado.
- Consulta de usuarios.

📦 Gestión de pedidos

- Registro de pedidos.
- Consulta de pedidos.

🖼️ Gestión de imágenes

- Carga de imágenes.
- Consulta de imágenes mediante su identificador.
- Procesamiento de imágenes.

🔐 Seguridad

- Autenticación mediante JWT.
- Protección de operaciones que requieren autorización.
- Configuración mediante variables de entorno.
- Control de acceso según los permisos establecidos.

---

💻 Tecnologías utilizadas

Las siguientes herramientas y tecnologías fueron utilizadas durante el desarrollo de TechGear:

Tecnología| Uso dentro del proyecto
Python| Lenguaje principal del backend.
Django| Desarrollo de la aplicación web.
FastAPI| Creación de la API REST.
MongoDB Atlas| Base de datos NoSQL en la nube.
Motor / PyMongo| Conexión y operaciones con MongoDB.
HTML5| Estructura de las páginas web.
CSS3| Diseño y estilos visuales.
JavaScript| Interactividad de la interfaz.
JWT| Autenticación y autorización.
Pillow| Procesamiento de imágenes.
Git| Control de versiones.
GitHub| Almacenamiento y colaboración en el código.
Render| Despliegue de la API.
Vercel| Despliegue de la aplicación web.

---

🏗️ Arquitectura del sistema

TechGear utiliza una arquitectura dividida en dos aplicaciones que se comunican entre sí.

                 USUARIO
                    |
                    v
           APLICACIÓN WEB
                DJANGO
                    |
                    v
                API REST
                FASTAPI
                    |
                    v
               MONGODB
                 ATLAS

Descripción de los componentes

Componente| Responsabilidad
Django| Gestiona la interfaz web, las vistas y las solicitudes del usuario.
FastAPI| Procesa las solicitudes y proporciona los servicios de la API REST.
MongoDB Atlas| Almacena la información utilizada por la API.
Render| Aloja el backend desarrollado con FastAPI.
Vercel| Aloja la aplicación web desarrollada con Django.

---

📁 Estructura del proyecto

El proyecto está organizado en dos módulos principales: el backend desarrollado con FastAPI y la aplicación web desarrollada con Django.

TechGear/
│
├── techgear_api/
│   │
│   ├── main.py
│   ├── requirements.txt
│   │
│   └── db/
│       └── database.py
│
├── techgear_web/
│   │
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
│       │
│       ├── templates/
│       │
│       └── static/
│
├── .gitignore
│
└── README.md

¿Qué contiene cada módulo?

1. "techgear_api/"

Contiene el backend desarrollado con FastAPI.

Archivo o carpeta| Descripción
"main.py"| Archivo principal de la API y definición de endpoints.
"requirements.txt"| Dependencias necesarias para ejecutar la API.
"db/"| Contiene los archivos relacionados con la conexión a la base de datos.
"database.py"| Configuración de conexión con MongoDB.

2. "techgear_web/"

Contiene la aplicación web desarrollada con Django.

Archivo o carpeta| Descripción
"manage.py"| Permite ejecutar comandos administrativos de Django.
"settings.py"| Configuración general del proyecto.
"urls.py"| Configuración de las rutas principales.
"asgi.py"| Configuración para servidores ASGI.
"wsgi.py"| Configuración para servidores WSGI.
"store/"| Aplicación encargada de las funcionalidades de la tienda.
"views.py"| Contiene las vistas de la aplicación.
"models.py"| Define los modelos de datos de Django.
"admin.py"| Configuración del panel administrativo.
"templates/"| Contiene las plantillas HTML.
"static/"| Contiene los archivos CSS, JavaScript e imágenes estáticas.

---

🛠️ Instalación y configuración

Para ejecutar el proyecto localmente, es necesario tener instalado:

- Python.
- Git.
- Visual Studio Code (recomendado).
- Una cuenta de MongoDB Atlas con una base de datos configurada.

1. Clonar el repositorio

git clone https://github.com/joseismael25/TechGear.git

Ingresar a la carpeta del proyecto:

cd TechGear

2. Configurar el backend FastAPI

Ingresar a la carpeta:

cd techgear_api

Crear un entorno virtual:

python -m venv venv

Activar el entorno virtual en Windows:

venv\Scripts\activate

Instalar las dependencias:

pip install -r requirements.txt

3. Configurar Django

Abrir otra terminal y dirigirse a la carpeta del proyecto Django:

cd techgear_web

Crear un entorno virtual:

python -m venv venv

Activar el entorno virtual:

venv\Scripts\activate

Instalar las dependencias:

pip install -r requirements.txt

---

🔑 Variables de entorno

El proyecto utiliza variables de entorno para configurar las conexiones y proteger la información sensible.

FastAPI

Crear un archivo ".env" dentro de la carpeta "techgear_api" con la siguiente configuración:

MONGO_URI=tu_url_de_mongodb
SECRET_KEY=tu_clave_secreta
ADMIN_EMAILS=correo_administrador
PUBLIC_API_URL=http://127.0.0.1:8000
CORS_ORIGINS=http://127.0.0.1:8001

Django

Configurar las variables correspondientes en el archivo ".env" de Django:

API_URL=http://127.0.0.1:8000
DJANGO_SECRET_KEY=tu_clave_secreta
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_SECURE_COOKIES=False

Importante: los archivos ".env" contienen información privada y no deben subirse al repositorio de GitHub.

---

▶️ Ejecución del proyecto

Para trabajar con la aplicación localmente, se deben ejecutar FastAPI y Django en terminales independientes.

1. Ejecutar FastAPI

Desde la carpeta "techgear_api", con el entorno virtual activado:

uvicorn main:app --reload

La API estará disponible en:

http://127.0.0.1:8000

Documentación interactiva:

http://127.0.0.1:8000/docs

2. Ejecutar Django

Desde la carpeta "techgear_web", con el entorno virtual activado:

python manage.py migrate

Después ejecutar:

python manage.py runserver 8001

La aplicación web estará disponible en:

http://127.0.0.1:8001

---

🔌 Endpoints de la API

La API REST de TechGear cuenta con los siguientes endpoints:

General

Método| Endpoint| Descripción
GET| "/"| Ruta principal de la API.

Autenticación

Método| Endpoint| Descripción
POST| "/auth/login"| Inicio de sesión.

Usuarios

Método| Endpoint| Descripción
POST| "/users"| Registro de usuarios.
GET| "/users/me"| Consulta del usuario autenticado.
GET| "/users"| Consulta de usuarios.

Imágenes

Método| Endpoint| Descripción
POST| "/images"| Carga de imágenes.
GET| "/images/{image_id}"| Consulta de una imagen.

Productos

Método| Endpoint| Descripción
POST| "/products"| Registro de productos.
GET| "/products"| Consulta de productos.
GET| "/products/{id}"| Consulta de un producto específico.
PUT| "/products/{id}"| Actualización de un producto.
DELETE| "/products/{id}"| Eliminación de un producto.

Pedidos

Método| Endpoint| Descripción
POST| "/orders"| Registro de pedidos.
GET| "/orders"| Consulta de pedidos.

---

☁️ Despliegue

El proyecto se encuentra desplegado utilizando servicios independientes para el backend y la aplicación web.

Servicio| Plataforma| Enlace
Aplicación web| Vercel| "Abrir TechGear" (https://tech-gear-kappa.vercel.app/)
Backend API| Render| "Abrir API" (https://techgear-yxm3.onrender.com/)
Documentación API| FastAPI / Render| "Ver documentación" (https://techgear-yxm3.onrender.com/docs)

---

🔄 Control de versiones

Para administrar los cambios del proyecto se utiliza Git y GitHub.

Comandos principales:

Consultar el estado de los archivos:

git status

Agregar cambios:

git add .

Crear un commit:

git commit -m "Descripción de los cambios"

Subir los cambios al repositorio:

git push origin main

Si se trabaja en otra rama, se debe reemplazar "main" por el nombre correspondiente.

---

👨‍💻 Información del proyecto

Nombre: TechGear

Tipo de proyecto: Aplicación web con API REST.

Backend: FastAPI.

Aplicación web: Django.

Base de datos: MongoDB Atlas.

Repositorio: "GitHub - TechGear" (https://github.com/joseismael25/TechGear)

---

<p align="center">
  <strong>TECHGEAR</strong>
  <br>
  Plataforma web para la gestión de productos y servicios tecnológicos.
  <br><br>
  Desarrollado como proyecto de formación.
</p>
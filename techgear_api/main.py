import hashlib
import hmac
import logging
import os
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from io import BytesIO

import jwt
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymongo.errors import DuplicateKeyError

load_dotenv(Path(__file__).resolve().parent / ".env")
logger = logging.getLogger(__name__)

if __package__:
    from .db.database import get_database
    from .models.schemas import (
        UserCreate, UserLogin, TokenResponse, UserResponse,
        ProductCreate, ProductUpdate, ProductResponse, OrderCreate, OrderResponse,
    )
else:
    # Permite ejecutar desde techgear_api con: uvicorn main:app --reload
    from db.database import get_database
    from models.schemas import (
        UserCreate, UserLogin, TokenResponse, UserResponse,
        ProductCreate, ProductUpdate, ProductResponse, OrderCreate, OrderResponse,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Comprueba la conexión al iniciar sin impedir que la API arranque."""
    try:
        db = get_database()
        await db.command("ping")
        await db["users"].create_index("email", unique=True)
        logger.info("Conexión exitosa a MongoDB Atlas.")
    except Exception:
        logger.exception("No fue posible conectar con MongoDB Atlas.")
    yield


app = FastAPI(
    title="TechGear API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://127.0.0.1:8001,http://localhost:8001").split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenido a TechGear API - Clase 2"}


# --- SEGURIDAD (JWT) ---
SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    logger.warning("SECRET_KEY no está configurada. Los endpoints JWT no funcionarán hasta configurarla.")
ALGORITHM = "HS256"
# Correos que obtienen rol admin (separados por coma). Ej: ADMIN_EMAILS=tu@correo.com
ADMIN_EMAILS = {e.strip().lower() for e in os.getenv("ADMIN_EMAILS", "").split(",") if e.strip()}
TOKEN_EXPIRE_MINUTES = 60
bearer_scheme = HTTPBearer()

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return f"{salt}${digest}"

def verify_password(password: str, stored: str) -> bool:
    try:
        salt, digest = stored.split("$")
    except ValueError:
        return False
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return hmac.compare_digest(check, digest)

def create_access_token(user_id: str, email: str, rol: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "rol": rol,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    }
    if not SECRET_KEY:
        raise HTTPException(status_code=503, detail="La autenticación no está configurada en el servidor")
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not SECRET_KEY:
        raise HTTPException(status_code=503, detail="La autenticación no está configurada en el servidor")
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    db = get_database()
    if not ObjectId.is_valid(payload.get("sub", "")):
        raise HTTPException(status_code=401, detail="Token inválido")
    user = await db["users"].find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

async def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol administrador")
    return current_user

def user_to_response(u: dict) -> dict:
    return {"id": str(u["_id"]), "nombre": u["nombre"], "email": u["email"], "rol": u["rol"]}

# --- AUTENTICACIÓN ---
@app.post("/auth/login", response_model=TokenResponse, tags=["Autenticación"])
async def login(credentials: UserLogin):
    db = get_database()
    user = await db["users"].find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user.get("password", "")):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    if user["email"].lower() in ADMIN_EMAILS and user.get("rol") != "admin":
        await db["users"].update_one({"_id": user["_id"]}, {"$set": {"rol": "admin"}})
        user["rol"] = "admin"
    token = create_access_token(str(user["_id"]), user["email"], user["rol"])
    return {"access_token": token, "token_type": "bearer"}

# --- USUARIOS ---
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
async def create_user(user: UserCreate):
    db = get_database()
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo")
    data = user.model_dump()
    data["password"] = hash_password(data["password"])
    # El rol lo decide el servidor: nadie puede registrarse como admin desde afuera
    data["rol"] = "admin" if user.email.lower() in ADMIN_EMAILS else "cliente"
    try:
        result = await db["users"].insert_one(data)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese correo")
    created = await db["users"].find_one({"_id": result.inserted_id})
    return user_to_response(created)

@app.get("/users/me", response_model=UserResponse, tags=["Usuarios"])
async def get_me(current_user: dict = Depends(get_current_user)):
    return user_to_response(current_user)

@app.get("/users", response_model=list[UserResponse], tags=["Usuarios"])
async def list_users(current_user: dict = Depends(require_admin)):
    db = get_database()
    users = []
    async for u in db["users"].find():
        users.append(user_to_response(u))
    return users

# --- IMÁGENES DE PRODUCTOS ---
MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
PUBLIC_API_URL = os.getenv("PUBLIC_API_URL", "http://127.0.0.1:8000").rstrip("/")

@app.post("/images", tags=["Imágenes"], status_code=status.HTTP_201_CREATED)
async def upload_product_image(image: UploadFile = File(...), admin: dict = Depends(require_admin)):
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa JPG, PNG o WebP.")
    content = await image.read(MAX_IMAGE_SIZE + 1)
    if not content or len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="La imagen debe pesar como máximo 5 MB.")
    try:
        with Image.open(BytesIO(content)) as img:
            expected_formats = {"image/jpeg": "JPEG", "image/png": "PNG", "image/webp": "WEBP"}
            if img.format != expected_formats[image.content_type]:
                raise HTTPException(status_code=400, detail="El contenido del archivo no coincide con su formato.")
            width, height = img.size
            if width > 6000 or height > 6000:
                raise HTTPException(status_code=400, detail="La imagen no puede superar 6000 x 6000 píxeles.")
            img.verify()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise HTTPException(status_code=400, detail="El archivo seleccionado no es una imagen válida.")
    db = get_database()
    result = await db["product_images"].insert_one({
        "data": content, "content_type": image.content_type,
        "filename": (image.filename or "producto")[:150],
        "created_at": datetime.now(timezone.utc),
    })
    image_url = f"{PUBLIC_API_URL}/images/{result.inserted_id}"
    return {"id": str(result.inserted_id), "image_url": image_url}

@app.get("/images/{image_id}", tags=["Imágenes"], include_in_schema=True)
async def get_product_image(image_id: str):
    if not ObjectId.is_valid(image_id):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    db = get_database()
    image = await db["product_images"].find_one({"_id": ObjectId(image_id)})
    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return Response(content=image["data"], media_type=image.get("content_type", "image/jpeg"),
                    headers={"Cache-Control": "public, max-age=86400", "X-Content-Type-Options": "nosniff"})


def product_to_response(product: dict) -> dict:
    return {
        "id": str(product["_id"]), "nombre": product["nombre"],
        "descripcion": product.get("descripcion", ""), "precio": product["precio"],
        "stock": product["stock"], "categoria": product["categoria"],
        "image_url": product.get("image_url"),
    }

# --- PRODUCTOS (CRUD) ---
@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Productos"])
async def create_product(product: ProductCreate, admin: dict = Depends(require_admin)):
    db = get_database()
    result = await db["products"].insert_one(product.model_dump())
    created = await db["products"].find_one({"_id": result.inserted_id})
    return product_to_response(created)

@app.get("/products", response_model=list[ProductResponse], tags=["Productos"])
async def get_products():
    db = get_database()
    products = []
    async for product in db["products"].find().sort("_id", -1):
        products.append(product_to_response(product))
    return products

@app.get("/products/{id}", response_model=ProductResponse, tags=["Productos"])
async def get_product(id: str):
    db = get_database()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    product = await db["products"].find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product_to_response(product)

@app.put("/products/{id}", response_model=ProductResponse, tags=["Productos"])
async def update_product(id: str, product_update: ProductUpdate, admin: dict = Depends(require_admin)):
    db = get_database()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    update_data = {k: v for k, v in product_update.model_dump().items() if v is not None}
    if update_data:
        await db["products"].update_one({"_id": ObjectId(id)}, {"$set": update_data})
    product = await db["products"].find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product_to_response(product)

@app.delete("/products/{id}", tags=["Productos"])
async def delete_product(id: str, admin: dict = Depends(require_admin)):
    db = get_database()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID no válido")
    result = await db["products"].delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado exitosamente"}

# --- PEDIDOS ---
@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
async def create_order(order: OrderCreate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    current_user_id = str(current_user["_id"])
    if order.usuario_id != current_user_id:
        raise HTTPException(status_code=403, detail="No puedes crear pedidos para otro usuario")
    # El servidor determina precios y existencias: nunca confía en importes enviados por el navegador.
    verified_items = []
    decremented = []
    total = 0.0
    for item in order.items:
        if not ObjectId.is_valid(item.product_id):
            for product_id, quantity in decremented:
                await db["products"].update_one(
                    {"_id": ObjectId(product_id)}, {"$inc": {"stock": quantity}}
                )
            raise HTTPException(status_code=400, detail="Producto no válido")
        product = await db["products"].find_one({"_id": ObjectId(item.product_id)})
        if not product or product.get("stock", 0) < item.cantidad:
            for product_id, quantity in decremented:
                await db["products"].update_one(
                    {"_id": ObjectId(product_id)}, {"$inc": {"stock": quantity}}
                )
            raise HTTPException(status_code=409, detail=f"Stock insuficiente para {product.get('nombre', 'un producto') if product else 'un producto'}")
        update = await db["products"].update_one(
            {"_id": ObjectId(item.product_id), "stock": {"$gte": item.cantidad}},
            {"$inc": {"stock": -item.cantidad}},
        )
        if update.modified_count != 1:
            for product_id, quantity in decremented:
                await db["products"].update_one(
                    {"_id": ObjectId(product_id)}, {"$inc": {"stock": quantity}}
                )
            raise HTTPException(status_code=409, detail="El stock cambió. Actualiza el catálogo e inténtalo de nuevo.")
        decremented.append((item.product_id, item.cantidad))
        unit_price = float(product["precio"])
        verified_items.append({
            "product_id": item.product_id,
            "cantidad": item.cantidad,
            "precio_unitario": unit_price,
        })
        total += item.cantidad * unit_price

    order_dict = {
        "usuario_id": current_user_id,
        "items": verified_items,
        "total": round(total, 2),
        "fecha": datetime.now(timezone.utc),
    }
    try:
        result = await db["orders"].insert_one(order_dict)
    except Exception:
        for product_id, quantity in decremented:
            await db["products"].update_one(
                {"_id": ObjectId(product_id)}, {"$inc": {"stock": quantity}}
            )
        raise
    created = await db["orders"].find_one({"_id": result.inserted_id})
    return {
        "id": str(created["_id"]),
        "usuario_id": created["usuario_id"],
        "items": created["items"],
        "total": created["total"],
        "fecha": created["fecha"]
    }

@app.get("/orders", response_model=list[OrderResponse], tags=["Pedidos"])
async def get_orders(current_user: dict = Depends(get_current_user)):
    db = get_database()
    orders = []
    query = {} if current_user.get("rol") == "admin" else {"usuario_id": str(current_user["_id"])}
    async for o in db["orders"].find(query).sort("fecha", -1):
        orders.append({
            "id": str(o["_id"]),
            "usuario_id": o["usuario_id"],
            "items": o["items"],
            "total": o["total"],
            "fecha": o["fecha"]
        })
    return orders
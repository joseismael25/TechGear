"""Esquemas y validaciones de entrada/salida de TechGear API."""
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("nombre")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre es obligatorio")
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    nombre: str
    email: EmailStr
    rol: str


class ProductCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: str = Field(default="", max_length=1000)
    precio: float = Field(gt=0, allow_inf_nan=False)
    stock: int = Field(ge=0)
    categoria: str = Field(min_length=1, max_length=80)
    image_url: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value):
        if value is None or value == "":
            return None
        parsed = urlparse(value)
        if not ((parsed.scheme in {"http", "https"} and parsed.netloc) or value.startswith("/images/")):
            raise ValueError("La imagen debe ser una URL http(s) válida o una imagen de TechGear")
        return value


class ProductUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    precio: Optional[float] = Field(default=None, gt=0, allow_inf_nan=False)
    stock: Optional[int] = Field(default=None, ge=0)
    categoria: Optional[str] = Field(default=None, min_length=1, max_length=80)
    image_url: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value):
        if value is None or value == "":
            return value
        parsed = urlparse(value)
        if not ((parsed.scheme in {"http", "https"} and parsed.netloc) or value.startswith("/images/")):
            raise ValueError("La imagen debe ser una URL http(s) válida o una imagen de TechGear")
        return value


class ProductResponse(BaseModel):
    id: str
    nombre: str
    descripcion: str
    precio: float
    stock: int
    categoria: str
    image_url: Optional[str] = None


class OrderItem(BaseModel):
    product_id: str = Field(min_length=1)
    cantidad: int = Field(gt=0)
    precio_unitario: float = Field(gt=0, allow_inf_nan=False)


class OrderCreate(BaseModel):
    usuario_id: str
    items: List[OrderItem] = Field(min_length=1)


class OrderResponse(BaseModel):
    id: str
    usuario_id: str
    items: List[OrderItem]
    total: float
    fecha: datetime

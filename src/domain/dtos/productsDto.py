from __future__ import annotations
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    """
    DTO para manejar las solicitudes relacionadas con productos (crear/actualizar).
    """
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    precio: Decimal = Field(..., ge=Decimal("0.00"))
    codigo_barras: Optional[str] = Field(None, max_length=100)
    stock_actual: int = Field(..., ge=0)
    categoria_id: UUID
    imagen_url: Optional[str] = Field(None, max_length=1000)
    estado: bool = True


class ProductResponse(BaseModel):
    """
    DTO para manejar las respuestas relacionadas con productos.
    """
    id: UUID
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    codigo_barras: Optional[str]
    stock_actual: int
    categoria_id: UUID
    imagen_url: Optional[str]
    estado: bool

    class Config:
        from_attributes = True  # Permite construir desde objetos con atributos (ORM, entidades, etc.)
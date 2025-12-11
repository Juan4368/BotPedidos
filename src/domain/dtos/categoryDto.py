from __future__ import annotations
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class CategoryRequest(BaseModel):
    """
    DTO para manejar las solicitudes relacionadas con categorias (crear/actualizar).
    """

    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None
    estado: bool = True


class CategoryResponse(BaseModel):
    """
    DTO para manejar las respuestas relacionadas con categorias.
    """

    id: UUID
    nombre: str
    descripcion: Optional[str]
    estado: bool

    model_config = {"from_attributes": True}

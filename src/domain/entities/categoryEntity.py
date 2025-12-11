from __future__ import annotations
from typing import Optional, Any
import uuid
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict


class CategoryEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `categories`.
    Configurada con `from_attributes=True` para aceptar objetos ORM o con atributos.
    """

    id: UUID = Field(default_factory=uuid.uuid4)
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None
    estado: bool = True

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
    )

    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    def update_nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacio")
        self.nombre = nuevo_nombre.strip()

    def update_descripcion(self, nueva_descripcion: Optional[str]) -> None:
        self.descripcion = nueva_descripcion.strip() if nueva_descripcion else None

    def set_estado(self, nuevo_estado: bool) -> None:
        self.estado = bool(nuevo_estado)

    @classmethod
    def from_model(cls, obj: Any) -> "CategoryEntity":
        return cls.model_validate(obj)

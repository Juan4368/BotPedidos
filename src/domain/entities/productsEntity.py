from __future__ import annotations
from decimal import Decimal
from typing import Optional, Any
import uuid
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict


class ProductEntity(BaseModel):
    """
    Entidad de dominio Pydantic v2 para la tabla `products`.
    Configurada con `from_attributes=True` para aceptar objetos ORM o con atributos.
    """
    id: UUID = Field(default_factory=uuid.uuid4)
    nombre: str = Field(..., min_length=1)
    descripcion: Optional[str] = None
    precio: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"))
    codigo_barras: Optional[str] = None
    stock_actual: int = Field(default=0, ge=0)
    categoria_id: UUID = Field(default_factory=uuid.uuid4)
    imagen_url: Optional[str] = None
    estado: bool = True

    # Configuración para Pydantic v2
    model_config = ConfigDict(
        from_attributes=True,        # Permite usar objetos con atributos (ORM)
        validate_assignment=True,    # Valida al asignar valores
        json_encoders={Decimal: lambda v: str(v), UUID: lambda v: str(v)},
    )

    # Validadores
    @field_validator("nombre", mode="before")
    def _strip_nombre(cls, v: Optional[str]) -> str:
        return (v or "").strip()

    @field_validator("precio", mode="before")
    def _ensure_decimal(cls, v) -> Decimal:
        if isinstance(v, Decimal):
            val = v
        else:
            val = Decimal(str(v or "0"))
        if val < 0:
            raise ValueError("El precio no puede ser negativo")
        return val

    @field_validator("stock_actual", mode="before")
    def _ensure_int_stock(cls, v) -> int:
        if v is None:
            return 0
        return int(v)

    @field_validator("categoria_id", mode="before")
    def _ensure_uuid_categoria(cls, v) -> UUID:
        if v is None:
            raise ValueError("El campo categoria_id es requerido")
        if isinstance(v, UUID):
            return v
        return UUID(str(v))

    # Lógica de negocio
    def increase_stock(self, qty: int) -> None:
        qty = int(qty)
        if qty <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        self.stock_actual += qty

    def decrease_stock(self, qty: int) -> None:
        qty = int(qty)
        if qty <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        if qty > self.stock_actual:
            raise ValueError("Stock insuficiente")
        self.stock_actual -= qty

    def is_active(self) -> bool:
        return bool(self.estado)

    # Interoperabilidad
    @classmethod
    def from_model(cls, obj: Any) -> "ProductEntity":
        """
        Construye la entidad desde un objeto con atributos (por ejemplo, una instancia de SQLAlchemy).
        """
        return cls.model_validate(obj)
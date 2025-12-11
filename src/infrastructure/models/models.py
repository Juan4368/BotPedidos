# ...existing code...
from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

# Try to use native UUID type for Postgres, fallback to String(36) for portability
try:
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID  # type: ignore

    UUID_TYPE = PG_UUID(as_uuid=True)
except Exception:
    UUID_TYPE = String(36)

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(Boolean, nullable=False, default=True)

    # relacion: una categoria tiene muchos productos
    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id!r}, nombre={self.nombre!r})>"


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("codigo_barras", name="uq_products_codigo_barras"),
    )

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)  # usa Decimal en Python
    codigo_barras = Column(String(100), nullable=True)
    stock_actual = Column(Integer, nullable=False, default=0)
    categoria_id = Column(UUID_TYPE, ForeignKey("categories.id"), nullable=False)
    imagen_url = Column(String(1000), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)

    # relacion: un producto pertenece a una categoria
    category = relationship("Category", back_populates="products", lazy="joined")

    # relacion opcional hacia OrderItem (si existe): un producto aparece en muchos items de pedido
    # order_items = relationship("OrderItem", back_populates="product", lazy="selectin")

    def precio_decimal(self) -> Decimal:
        return Decimal(self.precio)

    def __repr__(self) -> str:
        return f"<Product(id={self.id!r}, nombre={self.nombre!r}, precio={self.precio})>"
# ...existing code...

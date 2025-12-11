from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from decimal import Decimal

from sqlalchemy import or_
from sqlalchemy.orm import Session

from domain.entities.productsEntity import ProductEntity
from domain.interfaces.product_repository_interface import ProductRepositoryInterface
from infrastructure.models.models import Product


class ProductRepository(ProductRepositoryInterface):
    """Repositorio para manejar operaciones relacionadas con productos."""

    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_entity: ProductEntity) -> ProductEntity:
        """Crea un nuevo producto en la base de datos y devuelve la entidad."""
        product_orm = Product(
            id=product_entity.id,
            nombre=product_entity.nombre,
            descripcion=product_entity.descripcion,
            precio=product_entity.precio,
            codigo_barras=product_entity.codigo_barras,
            stock_actual=product_entity.stock_actual,
            categoria_id=product_entity.categoria_id,
            imagen_url=product_entity.imagen_url,
            estado=product_entity.estado,
        )

        self.db.add(product_orm)
        self.db.commit()
        self.db.refresh(product_orm)
        return ProductEntity.from_model(product_orm)

    def list_products(self) -> List[ProductEntity]:
        records = self.db.query(Product).all()
        return [ProductEntity.from_model(row) for row in records]

    def get_product(self, product_id: UUID) -> Optional[ProductEntity]:
        record = self.db.get(Product, product_id)
        if not record:
            return None
        return ProductEntity.from_model(record)

    def search_products(self, term: str) -> List[ProductEntity]:
        like_term = f"%{term}%"
        filters = [
            Product.nombre.ilike(like_term),
            Product.descripcion.ilike(like_term),
            Product.codigo_barras.ilike(like_term),
        ]

        try:
            price_value = Decimal(term)
            filters.append(Product.precio == price_value)
        except Exception:
            pass

        lowered = term.strip().lower()
        truthy = {"true", "1", "yes", "si", "on"}
        falsy = {"false", "0", "no", "off"}
        if lowered in truthy:
            filters.append(Product.estado.is_(True))
        elif lowered in falsy:
            filters.append(Product.estado.is_(False))

        records = self.db.query(Product).filter(or_(*filters)).all()
        return [ProductEntity.from_model(row) for row in records]

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from domain.entities.categoryEntity import CategoryEntity
from domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)
from infrastructure.models.models import Category


class CategoryRepository(CategoryRepositoryInterface):
    """Repositorio para operaciones de categorias."""

    def __init__(self, db: Session):
        self.db = db

    def create_category(self, category_entity: CategoryEntity) -> CategoryEntity:
        category_orm = Category(
            id=category_entity.id,
            nombre=category_entity.nombre,
            descripcion=category_entity.descripcion,
            estado=category_entity.estado,
        )
        self.db.add(category_orm)
        self.db.commit()
        self.db.refresh(category_orm)
        return CategoryEntity.from_model(category_orm)

    def list_categories(self) -> List[CategoryEntity]:
        records = self.db.query(Category).all()
        return [CategoryEntity.from_model(row) for row in records]

    def get_category(self, category_id: UUID) -> Optional[CategoryEntity]:
        record = self.db.get(Category, category_id)
        if not record:
            return None
        return CategoryEntity.from_model(record)

    def search_categories(self, term: str) -> List[CategoryEntity]:
        like_term = f"%{term}%"
        filters = [
            Category.nombre.ilike(like_term),
            Category.descripcion.ilike(like_term),
        ]

        lowered = term.strip().lower()
        truthy = {"true", "1", "yes", "si", "on"}
        falsy = {"false", "0", "no", "off"}
        if lowered in truthy:
            filters.append(Category.estado.is_(True))
        elif lowered in falsy:
            filters.append(Category.estado.is_(False))

        records = self.db.query(Category).filter(or_(*filters)).all()
        return [CategoryEntity.from_model(row) for row in records]

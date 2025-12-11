from __future__ import annotations
from typing import List, Optional
from uuid import UUID

from domain.dtos.categoryDto import CategoryRequest, CategoryResponse
from domain.entities.categoryEntity import CategoryEntity
from domain.interfaces.category_repository_interface import (
    CategoryRepositoryInterface,
)


class CategoryService:
    """Caso de uso para operaciones de categorias."""

    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    def create_category(self, data: CategoryRequest) -> CategoryResponse:
        entity = CategoryEntity(
            nombre=data.nombre,
            descripcion=data.descripcion,
            estado=data.estado,
        )
        created = self.repository.create_category(entity)
        return CategoryResponse.model_validate(created)

    def list_categories(self) -> List[CategoryResponse]:
        categorias = self.repository.list_categories()
        return [CategoryResponse.model_validate(cat) for cat in categorias]

    def get_category(self, category_id: UUID) -> Optional[CategoryResponse]:
        categoria = self.repository.get_category(category_id)
        if not categoria:
            return None
        return CategoryResponse.model_validate(categoria)

    def search_categories(self, term: str) -> List[CategoryResponse]:
        categorias = self.repository.search_categories(term)
        return [CategoryResponse.model_validate(cat) for cat in categorias]

from __future__ import annotations
from typing import List, Optional
from uuid import UUID

from domain.dtos.productsDto import ProductRequest, ProductResponse
from domain.entities.productsEntity import ProductEntity
from domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)


class ProductService:
    """Caso de uso para operaciones de productos."""

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def create_product(self, data: ProductRequest) -> ProductResponse:
        """Crea un producto usando el repositorio."""
        entity = ProductEntity(
            nombre=data.nombre,
            descripcion=data.descripcion,
            precio=data.precio,
            codigo_barras=data.codigo_barras,
            stock_actual=data.stock_actual,
            categoria_id=data.categoria_id,
            imagen_url=data.imagen_url,
            estado=data.estado,
        )
        created = self.repository.create_product(entity)
        return ProductResponse.model_validate(created)

    def list_products(self) -> List[ProductResponse]:
        productos = self.repository.list_products()
        return [ProductResponse.model_validate(prod) for prod in productos]

    def get_product(self, product_id: UUID) -> Optional[ProductResponse]:
        producto = self.repository.get_product(product_id)
        if not producto:
            return None
        return ProductResponse.model_validate(producto)

    def search_products(self, term: str) -> List[ProductResponse]:
        productos = self.repository.search_products(term)
        return [ProductResponse.model_validate(prod) for prod in productos]

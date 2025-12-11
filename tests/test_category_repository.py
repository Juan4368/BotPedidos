from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from domain.entities.categoryEntity import CategoryEntity
from infrastructure.models.models import Base, Category
from infrastructure.repository.createCategoryRepository import CategoryRepository


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def test_create_category_persists_and_returns_entity(db_session):
    repo = CategoryRepository(db_session)
    entity = CategoryEntity(nombre="Bebidas", descripcion="Productos frios")

    created = repo.create_category(entity)

    assert isinstance(created, CategoryEntity)
    assert created.nombre == "Bebidas"
    assert created.descripcion == "Productos frios"

    persisted = db_session.query(Category).one()
    assert str(persisted.id) == str(created.id)
    assert persisted.nombre == created.nombre
    assert persisted.descripcion == created.descripcion

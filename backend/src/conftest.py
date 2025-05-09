import asyncio
from contextlib import ExitStack

import pytest
import uuid
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from asyncpg import Connection
from httpx import AsyncClient, ASGITransport
from sqlalchemy import inspect, text, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session, DatabaseSessionManager
from db.models import (
    Base,
    DocumentType,
    NomenclatureType,
    NomenclatureGroup,
    MeasureUnit,
    Nomenclature, Recipe, BaseRecipe
)
from main import app as actual_app
from settings import get_settings
from constants import STANDARD_NOMENCLATURE_TYPES, STANDARD_NOMENCLATURE_GROUPS, STANDARD_MEASURE_UNITS, NOMENCLATURES

settings = get_settings()

sessionmanager = DatabaseSessionManager(settings.test_database_url, {"echo": settings.echo_sql})


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield actual_app


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def run_migrations(connection: Connection):
    config = Config("alembic.ini")
    config.set_main_option("script_location", "migrations")
    config.set_main_option("sqlalchemy.url", settings.test_database_url)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        print(f"⚙️  Upgrading from {rev} to head")
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(connection, opts={"target_metadata": Base.metadata, "fn": upgrade})

    inspector = inspect(connection)
    if "alembic_version" in inspector.get_table_names():
        connection.execute(text("DELETE FROM alembic_version"))

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with sessionmanager.connect() as connection:
        await connection.execute(text("DROP VIEW IF EXISTS stock_balance CASCADE"))
        await connection.run_sync(Base.metadata.drop_all)
        await connection.execute(text("DROP EXTENSION IF EXISTS pgcrypto CASCADE"))
        await connection.execute(text("DROP TRIGGER IF EXISTS set_document_number ON base_recipes CASCADE"))
        await connection.execute(text("DROP FUNCTION IF EXISTS public.increment_document_number() CASCADE"))

        await connection.run_sync(run_migrations)
    yield

    await sessionmanager.close()


@pytest.fixture(scope="module", autouse=True)
async def clean_database_per_module():
    async with sessionmanager.session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(delete(table))
        await session.commit()


        await session.execute(
            insert(NomenclatureType).values(STANDARD_NOMENCLATURE_TYPES)
        )
        await session.execute(
            insert(MeasureUnit).values(STANDARD_MEASURE_UNITS)
        )
        await session.execute(
            insert(NomenclatureGroup).values(STANDARD_NOMENCLATURE_GROUPS)
        )
        await session.execute(
            insert(Nomenclature).values(NOMENCLATURES)
        )
        await session.commit()


@pytest.fixture(scope="function", autouse=True)
async def transactional_session():
    async with sessionmanager.session() as session:
        try:
            await session.begin()
            yield session
        finally:
            await session.rollback()


@pytest.fixture(scope="function")
async def db_session():
    async with sessionmanager.session() as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, db_session):
    async def get_test_session():
        yield db_session

    app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="function")
async def get_data_for_recipe():
    async with sessionmanager.connect() as conn:
        nom_id = await conn.execute(
            select(Nomenclature.id)
            .where(Nomenclature.name == 'Эмаль ПФ-115')
        )


        return {'paint_id': nom_id.scalar_one()}

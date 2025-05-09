from typing import Any
from sqlalchemy import and_, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import datetime
import uuid

from db.models import DocumentType, BaseRecipe
from constants import DocumentTypesEnum, DocumentStatuses


class DocumentTypeDAL:
    """Data Access Layer for operating document types."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_document_type_by_id(self, type_id: uuid.UUID) -> DocumentType | None:
        query = select(DocumentType).where(DocumentType.id == type_id)
        result = await self.db_session.execute(query)
        result_row = result.fetchone()
        if result_row is not None:
            return result_row[0]

    async def get_document_type_by_name(self, name: str) -> DocumentType | None:
        query = select(DocumentType).where(DocumentType.name == name)
        result = await self.db_session.execute(query)
        result_row = result.fetchone()
        if result_row is not None:
            return result_row[0]

    async def get_all_document_types(self) -> list[DocumentType] | None:
        query = select(DocumentType)
        result = await self.db_session.execute(query)
        result_rows = result.fetchall()
        return [doc_type[0] for doc_type in result_rows]


class BaseRecipeDAL:
    """Data Access Layer for operating base recipes."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _get_document_type_id(self) -> uuid.UUID | None:
        type_dal = DocumentTypeDAL(self.db_session)
        type_id = await type_dal.get_document_type_by_name(DocumentTypesEnum.BaseRecipeType)
        if type_id:
            return type_id.id

    async def create_base_recipe(
        self,
        status: DocumentStatuses,
        document_datetime: datetime.datetime,
        commentary: str,
        rules: dict[str, Any] | None,
        name: str | None = None
    ) -> BaseRecipe:
        doc_type_id = await self._get_document_type_id()
        if doc_type_id is None:
            raise ValueError('Cannot create base recipe: BaseRecipe type does not exist.')

        new_rec = BaseRecipe(
            status=status,
            document_datetime=document_datetime,
            commentary=commentary or "",
            rules=rules or {},
            document_type_id=doc_type_id,
            name=name
        )
        self.db_session.add(new_rec)
        await self.db_session.flush()
        await self.db_session.refresh(new_rec)
        return new_rec

    async def delete_base_recipe(self, id: uuid.UUID):
        query = (
            delete(BaseRecipe).where(BaseRecipe.id == id)
            .returning(BaseRecipe.id, BaseRecipe.document_number, BaseRecipe.name, BaseRecipe.document_datetime)
        )
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.fetchone()

    async def get_base_recipe_by_id(self, id: uuid.UUID) -> BaseRecipe | None:
        query = select(BaseRecipe).where(BaseRecipe.id == id)
        result = await self.db_session.execute(query)
        result_row = result.fetchone()
        if result_row is not None:
            return result_row[0]

    async def get_all_base_recipes(self) -> list[BaseRecipe] | None:
        query = select(BaseRecipe).order_by(BaseRecipe.document_datetime).order_by(BaseRecipe.document_number)
        result = await self.db_session.execute(query)
        result_rows = result.fetchall()
        return [row[0] for row in result_rows]


    async def update_base_recipe(self, id: uuid.UUID, **kwargs) -> BaseRecipe | None:
        query = (
            update(BaseRecipe)
            .where(BaseRecipe.id == id)
            .values(kwargs)
            .returning(BaseRecipe)
        )

        result = await self.db_session.execute(query)
        result_row = result.fetchone()
        if result_row is not None:
            return result_row[0]

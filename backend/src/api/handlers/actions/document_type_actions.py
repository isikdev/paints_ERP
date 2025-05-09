import uuid
from db.models import DocumentType
from db.dals import DocumentTypeDAL

from constants import DocumentTypesEnum
from sqlalchemy.ext.asyncio import AsyncSession

class DocumentTypeActions:
    """Class containing actions for document types, i.e. logic of session context managers and DAL calls."""
    DAL = DocumentTypeDAL

    @classmethod
    async def get_document_type_by_id(cls, document_type_id: uuid.UUID, session: AsyncSession) -> DocumentType | None:
        async with session.begin():
            doc_type_dal = cls.DAL(db_session=session)
            return await doc_type_dal.get_document_type_by_id(type_id=document_type_id)

    @classmethod
    async def get_document_type_by_name(cls, name: DocumentTypesEnum, session: AsyncSession) -> DocumentType | None:
        async with session.begin():
            doc_type_dal = cls.DAL(db_session=session)
            return await doc_type_dal.get_document_type_by_name(name=name)

    @classmethod
    async def get_all_document_types(cls, session: AsyncSession) -> list[DocumentType]:
        async with session.begin():
            doc_type_dal = cls.DAL(db_session=session)
            return await doc_type_dal.get_all_document_types()

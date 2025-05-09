from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import DocumentTypeReadResponse
from api.handlers.actions import DocumentTypeActions
from db import get_session


document_type_router = APIRouter(prefix="/document-types", tags=["Хэндлеры для DocumentType"])


@document_type_router.get('/', response_model=list[DocumentTypeReadResponse])
async def get_all_doc_types(session: AsyncSession = Depends(get_session)):
    doc_types = await DocumentTypeActions.get_all_document_types(session=session)
    return doc_types

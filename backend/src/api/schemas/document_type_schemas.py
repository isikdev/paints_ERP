import uuid
from constants import DocumentTypesEnum

from .base_models import BaseModel, ResponseModel


class DocumentTypeReadResponse(ResponseModel):
    """Scheme describing how to respond to DocumentType reading request."""
    id: uuid.UUID
    name: DocumentTypesEnum


class DocumentTypeReadRequest(BaseModel):
    """Scheme for validating DocumentType reading request."""
    id_or_name: uuid.UUID | DocumentTypesEnum

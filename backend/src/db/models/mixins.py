from sqlalchemy.orm import declared_attr, Mapped, relationship, mapped_column
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import Boolean

from .type_annotaions import (
    document_name, uuid_pk, document_type_fk, document_number,
    document_status_name, created_at, document_datetime, text_type
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .document_type import DocumentType


class AbstractDocumentMixin:
    id: Mapped[uuid_pk]
    document_number: Mapped[document_number]
    status: Mapped[document_status_name]
    created_at: Mapped[created_at]
    document_datetime: Mapped[document_datetime]
    name: Mapped[document_name]
    commentary: Mapped[text_type]
    document_type_id: Mapped[document_type_fk]

    @declared_attr
    def document_type(cls) -> Mapped["DocumentType"]:
        return relationship("DocumentType")

from sqlalchemy.orm import Mapped
from sqlalchemy.schema import UniqueConstraint

from .type_annotaions import type_name, uuid_pk, document_type_counter_fk, year, counter
from .base_model import Base


class DocumentType(Base):
    """Class representing a document type."""
    __tablename__ = "document_types"

    id: Mapped[uuid_pk]
    name: Mapped[type_name]
    direction: Mapped[int]


class DocumentNumberCounter(Base):
    __tablename__ = "document_number_counters"

    id: Mapped[uuid_pk]
    document_type_id: Mapped[document_type_counter_fk]
    year: Mapped[year]
    counter: Mapped[counter]

    __table_args__ = (
        UniqueConstraint("document_type_id", "year", name="_unique_document_type_year_uc"),
    )

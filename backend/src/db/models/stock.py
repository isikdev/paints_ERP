import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship
from .base_model import Base
from .mixins import AbstractDocumentMixin
from .nomenclature import Nomenclature
from .nomenclature_type import NomenclatureType


class Document(AbstractDocumentMixin, Base):
    """Заголовок любого склада‑документа."""

    __tablename__ = "documents"

    lines: Mapped[list["DocumentLine"]] = relationship(back_populates="document", cascade="all, delete-orphan")


class DocumentLine(Base):
    """Строка документа."""

    __tablename__ = "document_lines"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    document: Mapped[Document] = relationship(back_populates="lines")

    nomenclature_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nomenclatures.id"))
    nomenclature: Mapped[Nomenclature] = relationship()

    qty: Mapped[Decimal] = mapped_column(Numeric(18, 4))  # + приход, – расход

    __table_args__ = (UniqueConstraint("document_id", "nomenclature_id", name="uq_docline_nom"),)


class StockMove(Base):
    __tablename__ = "stock_moves"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_line_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document_lines.id", ondelete="CASCADE"), unique=True)
    document_line: Mapped[DocumentLine] = relationship()

    nomenclature_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nomenclatures.id"))
    nomenclature: Mapped[Nomenclature] = relationship()

    qty: Mapped[Decimal] = mapped_column(Numeric(18, 4))
    document_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<Move {self.nomenclature_id} {self.qty}>"

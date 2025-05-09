from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from sqlalchemy import UniqueConstraint, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

import uuid

from .base_model import Base
from .type_annotaions import uuid_pk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .nomenclature import Nomenclature


class NomenclatureGroup(Base):
    __tablename__ = "nomenclature_groups"
    __table_args__ = (
        UniqueConstraint("parent_id", "name", name="uq_nomenclature_group_parent_name"),
    )

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("nomenclature_groups.id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )

    @declared_attr
    def parent(cls) -> Mapped["NomenclatureGroup"]:
        return relationship(
            "NomenclatureGroup",
            remote_side="NomenclatureGroup.id",
            back_populates="children"
        )

    @declared_attr
    def children(cls) -> Mapped[list["NomenclatureGroup"]]:
        return relationship(
            "NomenclatureGroup",
            back_populates="parent"
        )

    @declared_attr
    def nomenclatures(cls) -> Mapped[list["Nomenclature"]]:
        return relationship(
            "Nomenclature",
            back_populates="group"
        )

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

from typing import TYPE_CHECKING

from .base_model import Base
from .type_annotaions import uuid_pk

if TYPE_CHECKING:
    from .nomenclature import Nomenclature


class NomenclatureType(Base):
    __tablename__ = "nomenclature_types"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    @declared_attr
    def nomenclatures(cls) -> Mapped[list["Nomenclature"]]:
        return relationship(
            "Nomenclature",
            back_populates="type"
        )

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from sqlalchemy.dialects.postgresql import UUID

from decimal import Decimal
import uuid

from .base_model import Base
from .type_annotaions import uuid_pk

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .recipe import Recipe
    from .nomenclature import Nomenclature


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[uuid_pk]
    recipe_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False
    )
    nomenclature_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("nomenclatures.id", ondelete="RESTRICT"),
        nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(7, 2),
        nullable=False
    )

    @declared_attr
    def recipe(cls) -> Mapped["Recipe"]:
        return relationship(
            "Recipe",
            back_populates="ingredients"
        )

    @declared_attr
    def nomenclature(cls) -> Mapped["Nomenclature"]:
        return relationship(
            "Nomenclature",
            back_populates="ingredients"
        )

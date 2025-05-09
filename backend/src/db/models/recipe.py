import uuid

from decimal import Decimal
from typing import Annotated, TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped, declared_attr

from .type_annotaions import uuid_pk
from .base_model import Base
from .mixins import AbstractDocumentMixin

if TYPE_CHECKING:
    from .base_recipe import BaseRecipe
    from .nomenclature import Nomenclature
    from .ingredient import Ingredient


class Recipe(AbstractDocumentMixin, Base):
    __tablename__ = "recipes"
    __table_args__ = (
        UniqueConstraint("name", "document_number", name="_unique_recipe_name_number_uc"),
    )

    base_recipe_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("base_recipes.id", ondelete='CASCADE'), nullable=False
    )
    nomenclature_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("nomenclatures.id", ondelete='RESTRICT'), nullable=False
    )
    batch_amount: Mapped[Decimal] = mapped_column(Numeric(7, 2), nullable=False)

    @declared_attr
    def nomenclature(cls) -> Mapped["Nomenclature"]:
        return relationship("Nomenclature", back_populates="recipes")

    @declared_attr
    def base_recipe(cls) -> Mapped["BaseRecipe"]:
        return relationship("BaseRecipe", back_populates="recipes")

    @declared_attr
    def ingredients(cls) -> Mapped["Ingredient"]:
        return relationship("Ingredient", back_populates="recipe")


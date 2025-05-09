from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, declared_attr

from .type_annotaions import rules
from .base_model import Base
from .mixins import AbstractDocumentMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .recipe import Recipe
    from .nomenclature import Nomenclature

nomenclature_base_recipe_association = Table(
    "nomenclature_base_recipe_association",
    Base.metadata,
    Column("base_recipe_id", ForeignKey("base_recipes.id", ondelete="CASCADE"), primary_key=True),
    Column("nomenclature_id", ForeignKey("nomenclatures.id", ondelete="CASCADE"), primary_key=True),
)


class BaseRecipe(AbstractDocumentMixin, Base):
    __tablename__ = "base_recipes"
    __table_args__ = (
        UniqueConstraint("name", "document_number", name="_unique_base_recipe_name_number_uc"),
    )
    rules: Mapped[rules]

    @declared_attr
    def recipes(cls) -> Mapped[list["Recipe"]]:
        return relationship(
            "Recipe",
            back_populates="base_recipe"
        )

    @declared_attr
    def nomenclatures(cls) -> Mapped[list["Nomenclature"]]:
        return relationship(
            "Nomenclature",
            secondary=nomenclature_base_recipe_association,
            back_populates="base_recipes"
        )

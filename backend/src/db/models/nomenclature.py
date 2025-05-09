import uuid
from datetime import date
from sqlalchemy import String, Text, Date, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from .base_model import Base
from .base_recipe import nomenclature_base_recipe_association
from .type_annotaions import uuid_pk, text_type

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .measure_unit import MeasureUnit
    from .nomenclature_type import NomenclatureType
    from .nomenclature_group import NomenclatureGroup
    from .ingredient import Ingredient
    from .recipe import Recipe
    from .base_recipe import BaseRecipe

class Nomenclature(Base):
    __tablename__ = "nomenclatures"
    __table_args__ = (
        UniqueConstraint("group_id", "name", name="uq_nomenclature_group_name"),
    )

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    description: Mapped[text_type]
    sku: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        unique=True
    )
    barcode: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        unique=True
    )
    expiration_date: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )
    properties: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict
    )

    measure_unit_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("measure_units.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    type_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("nomenclature_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("nomenclature_groups.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    @declared_attr
    def measure_unit(cls) -> Mapped["MeasureUnit"]:
        return relationship(
            "MeasureUnit",
            back_populates="nomenclatures"
        )

    @declared_attr
    def type(cls) -> Mapped["NomenclatureType"]:
        return relationship(
            "NomenclatureType",
            back_populates="nomenclatures"
        )

    @declared_attr
    def group(cls) -> Mapped["NomenclatureGroup"]:
        return relationship(
            "NomenclatureGroup",
            back_populates="nomenclatures"
        )

    @declared_attr
    def ingredients(cls) -> Mapped[list["Ingredient"]]:
        return relationship(
            "Ingredient",
            back_populates="nomenclature"
        )

    @declared_attr
    def recipes(cls) -> Mapped[list["Recipe"]]:
        return relationship(
            "Recipe",
            back_populates="nomenclature"
        )

    @declared_attr
    def base_recipes(cls) -> Mapped[list["BaseRecipe"]]:
        return relationship(
            "BaseRecipe",
            secondary=nomenclature_base_recipe_association,
            back_populates="nomenclatures"
        )

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

import uuid

from .base_model import Base


class RecipeGenerationSettings(Base):
    __tablename__ = "recipe_generation_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)

    film_formers_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("nomenclature_groups.id", ondelete="RESTRICT"),
        nullable=True
    )
    pigments_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("nomenclature_groups.id", ondelete="RESTRICT"),
        nullable=True
    )
    fillers_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("nomenclature_groups.id", ondelete="RESTRICT"),
        nullable=True
    )

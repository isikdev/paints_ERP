import datetime
import uuid
from typing import Annotated

from pydantic import Field, PositiveInt, PositiveFloat

from constants import DocumentStatuses
from .base_models import BaseModel, ResponseModel

DocumentDatetime = Annotated[datetime.datetime | None, Field(default_factory=datetime.datetime.now)]
DocumentNumber = Annotated[PositiveInt | None, Field(description="Serial number of document inside its year")]
RecipeName = Annotated[str | None, Field(default=None)]
RecipeCommentary = Annotated[str | None, Field(default='')]


class Ingredients(ResponseModel):
    id: uuid.UUID
    amount: PositiveFloat


class RecipeCreateRequest(BaseModel):
    status: DocumentStatuses = DocumentStatuses.Posted
    document_datetime: DocumentDatetime
    commentary: RecipeCommentary
    name: RecipeName

    nomenclature_id: uuid.UUID
    base_recipe_id: uuid.UUID
    planned_quantity: PositiveFloat


class RecipeUpdateRequest(BaseModel):
    status: DocumentStatuses = None # может быть None, Posted или SetToDeletion
    document_datetime: DocumentDatetime = None
    commentary: RecipeCommentary
    name: RecipeName

    nomenclature_id: uuid.UUID | None = None
    base_recipe_id: uuid.UUID | None = None
    planned_quantity: PositiveFloat | None = None
    ingredients: list[Ingredients] | None = None


class RecipeResponse(ResponseModel):
    """Ответ для создания, получения и обновления."""
    id: uuid.UUID
    document_number: DocumentNumber
    status: DocumentStatuses = DocumentStatuses.Posted # может быть Posted или SetToDeletion
    document_datetime: DocumentDatetime
    commentary: RecipeCommentary
    name: RecipeName

    nomenclature_id: uuid.UUID
    base_recipe_id: uuid.UUID
    ingredients: list[Ingredients]

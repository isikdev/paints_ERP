import datetime
import uuid
from typing import Annotated, Self

from pydantic import model_validator, Field, PositiveInt

from constants import DocumentStatuses, BASE_RECIPE_BODY_EXAMPLE
from .base_models import BaseModel, ResponseModel
from .rules_schemas import Rules

DocumentDatetime = Annotated[datetime.datetime | None, Field(default_factory=datetime.datetime.now)]
DocumentNumber = Annotated[PositiveInt | None, Field(description="Serial number of document inside its year")]
BaseRecipeName = Annotated[str | None, Field(default=None)]
BaseRecipeCommentary = Annotated[str | None, Field(default=None)]


class BaseRecipeCreateRequest(BaseModel):
    """Scheme for validating BaseRecipe creation request."""
    status: DocumentStatuses = DocumentStatuses.Registered
    document_datetime: DocumentDatetime
    commentary: BaseRecipeCommentary = ''
    name: BaseRecipeName
    rules: Rules | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                BASE_RECIPE_BODY_EXAMPLE
            ]
        }
    }

    @model_validator(mode="before")
    def _empty_rules_to_none(cls, values: dict) -> dict:
        status = values.get("status")
        if status == DocumentStatuses.Posted.value or status == DocumentStatuses.Posted:
            if values.get("rules") == {}:
                values["rules"] = None
        return values

    @model_validator(mode="after")
    def _empty_comment_if_none(self) -> Self:
        if self.commentary is None:
            self.commentary = ""
        return self


class BaseRecipeCreateResponse(ResponseModel):
    """Scheme describing how to respond to DocumentType creation request."""
    id: uuid.UUID
    document_number: int
    status: DocumentStatuses
    document_datetime: DocumentDatetime
    name: BaseRecipeName
    commentary: BaseRecipeCommentary
    rules: Rules | dict | None = Field(default_factory=dict)


class BaseRecipeReadRequest(BaseModel):
    """Scheme for validating BaseRecipe reading request."""
    id: uuid.UUID


class BaseRecipeReadResponse(ResponseModel):
    """Scheme describing how to respond to DocumentType reading request."""
    id: uuid.UUID
    document_number: int
    status: DocumentStatuses
    document_datetime: DocumentDatetime
    name: BaseRecipeName
    commentary: BaseRecipeCommentary
    rules: Rules | dict


class BaseRecipeUpdateRequest(BaseModel):
    """Scheme for validating BaseRecipe update request."""
    status: DocumentStatuses | None = None
    document_datetime: datetime.datetime | None = None
    name: BaseRecipeName
    commentary: BaseRecipeCommentary
    rules: Rules | None = None


class BaseRecipeUpdateResponse(ResponseModel):
    """Scheme describing how to respond to DocumentType update request."""
    id: uuid.UUID
    document_number: int
    status: DocumentStatuses
    document_datetime: DocumentDatetime
    name: BaseRecipeName
    commentary: BaseRecipeCommentary
    rules: Rules | dict | None = Field(default_factory=dict)


class BaseRecipeDeleteRequest(BaseModel):
    """Scheme for validating BaseRecipe deletion request."""
    id: uuid.UUID


class BaseRecipeDeleteResponse(ResponseModel):
    """Scheme describing how to respond to DocumentType deletion request."""
    id: uuid.UUID
    document_number: int
    name: BaseRecipeName
    document_datetime: DocumentDatetime

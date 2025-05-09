import uuid

from sqlalchemy import select, func
from typing import Annotated
from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import (
    BaseRecipeCreateResponse, BaseRecipeCreateRequest,
    BaseRecipeReadResponse,
    BaseRecipeUpdateResponse, BaseRecipeUpdateRequest,
    BaseRecipeDeleteResponse,
)
from api.handlers.actions import BaseRecipeActions
from db import get_session
from api.schemas.base_models import BaseModel

from constants import DocumentStatuses
from decimal import Decimal
from pydantic import BaseModel, field_validator, Field, conlist
from uuid import UUID as PydanticUUID
import datetime
from typing import Any
from copy import deepcopy
from api.schemas.rules_schemas import Rules

from db.models import Nomenclature, BaseRecipe, StockMove, NomenclatureGroup
from db.models.recipe_generation_settings import RecipeGenerationSettings
from constants import DosageTypeEnum

import logging

logger = logging.getLogger(__name__)



class IngredientModel(BaseModel):
    material_uuid: PydanticUUID
    amount: Decimal

    class Config:
        schema_extra = {"example": {"material_uuid": "00000000-0000-0000-0000-000000000000", "amount": 123.45}}

class RecipeModel(BaseModel):
    id: PydanticUUID = uuid.uuid4()
    nomenclature_id: PydanticUUID
    base_recipe_id: PydanticUUID
    ingredients: list[IngredientModel] = []
    document_datetime: datetime.datetime = datetime.datetime.now()


PositiveDecimal = Annotated[Decimal, Field(gt=0)]


class GenerateRecipeRequest(BaseModel):
    base_recipe_id: PydanticUUID
    nomenclature_id: PydanticUUID
    batch_size: PositiveDecimal


class Dosage(BaseModel):
    type: DosageTypeEnum
    value: PositiveDecimal


class Properties(BaseModel):
    color: str | None = None
    dosage: Dosage | None = None


recipe_router = APIRouter(prefix="/recipe", tags=["Хэндлеры для Recipe"])

import logging
logger = logging.getLogger()

@recipe_router.post('/', response_model=RecipeModel)
async def create_recipe(body: GenerateRecipeRequest, session: AsyncSession = Depends(get_session)) -> RecipeModel:
    res = await session.execute(select(Nomenclature).where(Nomenclature.id == body.nomenclature_id))
    nomenclature = res.scalars().first()
    if nomenclature is None:
        raise HTTPException(status_code=404, detail='nomenclature not found')
    properties = Properties(**nomenclature.properties)
    color = properties.color
    if color is None:
        raise HTTPException(status_code=422, detail='nomenclature must have color property')

    res = await session.execute(select(BaseRecipe).where(BaseRecipe.id == body.base_recipe_id))
    base_recipe = res.scalars().first()
    if base_recipe is None:
        raise HTTPException(status_code=404, detail='base recipe not found')
    if base_recipe.status != 'Posted':
        raise HTTPException(status_code=422, detail='base recipe must be posted')

    rules = Rules(**base_recipe.rules)

    color_data = None
    for c_d in rules.pigment_part:
        if c_d.color.lower() == color.lower():
            color_data = c_d
            break
    if color_data is None:
        raise HTTPException(status_code=422, detail=f'there is no rules for color {color} in base recipe')

    res = await session.execute(select(RecipeGenerationSettings).where(RecipeGenerationSettings.id == 1))
    settings = res.scalars().first()
    if settings is None:
        raise HTTPException(status_code=422, detail=f'set recipe generation settings on SETTINGS page')

    film_formers_common = rules.film_former_part.materials.root
    film_formers = []

    for m_d in color_data.materials:
        if m_d.nomenclature_group_id == settings.film_formers_group_id:
            film_formers.extend(m_d.items.root)
    film_formers.extend(film_formers_common)

    film_formers_available = []
    for item in film_formers:
        q = await session.execute(
            select(
                StockMove.nomenclature_id,
                func.coalesce(func.sum(StockMove.qty), 0).label("balance")
            )
            .where(StockMove.nomenclature_id.in_(item.uuids))
            .group_by(StockMove.nomenclature_id)
        )
        rows = q.all()
        balances: dict[uuid.UUID, Decimal] = {nom_id: balance for nom_id, balance in rows}
        film_formers_available.extend([u for u in item.uuids if balances.get(u, Decimal(0)) > 0])

    if not film_formers_available:
        raise HTTPException(
            status_code=422,
            detail="there are no film formers available in stock"
        )

    pigments = []
    for block in color_data.materials:
        if block.nomenclature_group_id == settings.pigments_group_id:
            pigments.extend(block.items.root)

    pigments_available = []
    for item in pigments:
        q = await session.execute(
            select(
                StockMove.nomenclature_id,
                func.coalesce(func.sum(StockMove.qty), 0).label("balance")
            )
            .where(StockMove.nomenclature_id.in_(item.uuids))
            .group_by(StockMove.nomenclature_id)
        )
        rows = q.all()
        balances: dict[uuid.UUID, Decimal] = {nom_id: balance for nom_id, balance in rows}
        pigments_available.extend([u for u in item.uuids if balances.get(u, Decimal(0)) > 0])

    if not pigments_available:
        raise HTTPException(
            status_code=422,
            detail="there are no pigments available in stock"
        )

    fillers = []
    for block in color_data.materials:
        if block.nomenclature_group_id == settings.fillers_group_id:
            fillers.extend(block.items.root)

    fillers_available = []
    for item in fillers:
        q = await session.execute(
            select(
                StockMove.nomenclature_id,
                func.coalesce(func.sum(StockMove.qty), 0).label("balance")
            )
            .where(StockMove.nomenclature_id.in_(item.uuids))
            .group_by(StockMove.nomenclature_id)
        )
        rows = q.all()
        balances: dict[uuid.UUID, Decimal] = {nom_id: balance for nom_id, balance in rows}
        fillers_available.extend([u for u in item.uuids if balances.get(u, Decimal(0)) > 0])

    if not fillers_available:
        raise HTTPException(
            status_code=422,
            detail="there are no fillers available in stock"
        )

    additives_part = rules.additives_part.materials
    additives = []
    for group in additives_part:
        group_items = []
        for m_d in color_data.materials:
            if m_d.nomenclature_group_id == group.nomenclature_group_id:
                group_items.extend(m_d.items.root)
        group_items.extend(group.items.root)

        group_available = []
        for item in group_items:
            q = await session.execute(
                select(
                    StockMove.nomenclature_id,
                    func.coalesce(func.sum(StockMove.qty), 0).label("balance")
                )
                .where(StockMove.nomenclature_id.in_(item.uuids))
                .group_by(StockMove.nomenclature_id)
            )
            rows = q.all()
            balances: dict[uuid.UUID, Decimal] = {nom_id: balance for nom_id, balance in rows}
            group_available.extend([u for u in item.uuids if balances.get(u, Decimal(0)) > 0])
        res = await session.execute(
            select(NomenclatureGroup.name).where(NomenclatureGroup.id == group.nomenclature_group_id)
        )
        group_name = res.scalars().first()
        if not group_available:
            raise HTTPException(
                status_code=422,
                detail=f"there are no {group_name} available in stock"
            )
        additives.append(group_available)

    print(additives)


    return RecipeModel(nomenclature_id=body.nomenclature_id, base_recipe_id=body.base_recipe_id)

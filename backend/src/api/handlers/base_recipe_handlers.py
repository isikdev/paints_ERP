import uuid

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException
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

from constants import DocumentStatuses

base_recipe_router = APIRouter(prefix="/document/base-recipe", tags=["Хэндлеры для BaseRecipe"])


@base_recipe_router.post('/', response_model=BaseRecipeCreateResponse)
async def create_base_recipe(body: BaseRecipeCreateRequest, session: AsyncSession = Depends(get_session)):
    if body.status == DocumentStatuses.Posted:
        await BaseRecipeActions.validate_body(body.model_dump(), session)
    try:
        return await BaseRecipeActions.create_base_recipe(body, session)
    except IntegrityError as e:
        if UniqueViolationError.__name__ in str(e.orig):
            raise HTTPException(status_code=409, detail="Base recipe with the same name already exists.")
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@base_recipe_router.get('/', response_model=BaseRecipeReadResponse)
async def get_base_recipe(base_recipe_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    base_recipe = await BaseRecipeActions.get_base_recipe(base_recipe_id, session)
    if not base_recipe:
        raise HTTPException(status_code=404, detail="Requested base recipe does not exist.")
    return base_recipe


@base_recipe_router.get('s/', response_model=list[BaseRecipeReadResponse])
async def get_all_base_recipes(session: AsyncSession = Depends(get_session)):
    return await BaseRecipeActions.get_all_base_recipes(session)


@base_recipe_router.patch('/', response_model=BaseRecipeUpdateResponse)
async def update_base_recipe(base_recipe_id: uuid.UUID, body: BaseRecipeUpdateRequest,
                          session: AsyncSession = Depends(get_session)):
    try:
        base_recipe = await BaseRecipeActions.get_base_recipe(base_recipe_id=base_recipe_id, session=session)
        if not base_recipe:
            raise HTTPException(status_code=404, detail="Updating base recipe does not exist.")
    except IntegrityError as e:
        raise HTTPException(status_code=503, detail=str(e))

    updates = body.model_dump(exclude_none=True, exclude={"rules"})
    if body.rules is not None:
        updates["rules"] = body.model_dump(include={"rules"})["rules"]

    if not updates:
        raise HTTPException(
            status_code=422, detail="At least one parameter for user update info should be provided"
        )

    need_rules_validation = (
            base_recipe.status == DocumentStatuses.Posted
            or updates.get("status") == DocumentStatuses.Posted
    )
    if need_rules_validation:
        if updates.get("rules") is None:
            updates["rules"] = base_recipe.rules
        await BaseRecipeActions.validate_body(updates, session)
    try:
        return await BaseRecipeActions.update_base_recipe(base_recipe_id, updates, session)
    except IntegrityError as e:
        raise HTTPException(status_code=503, detail=str(e))


@base_recipe_router.delete('/', response_model=BaseRecipeDeleteResponse)
async def delete_base_recipe(base_recipe_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    deleted_base_recipe = await BaseRecipeActions.delete_base_recipe(base_recipe_id, session)
    if not deleted_base_recipe:
        raise HTTPException(status_code=404, detail='Base recipe does not exist.')
    return deleted_base_recipe

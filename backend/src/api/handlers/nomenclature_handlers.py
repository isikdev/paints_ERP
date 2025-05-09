from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.nomenclature import NomenclatureListResponse, NomenclatureResponse, NomenclatureCreate, NomenclatureUpdate
from api.services.nomenclature import NomenclatureService
from db.models import User
from api.handlers.actions.auth import get_current_user_from_token
from db import get_session

router = APIRouter(prefix="/nomenclatures", tags=["nomenclatures"])


@router.get("/", response_model=NomenclatureListResponse)
async def get_all_nomenclatures(
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    service = NomenclatureService(db)
    nomenclatures = await service.get_all()
    return NomenclatureListResponse(nomenclatures=nomenclatures)


@router.get("/{nomenclature_id}", response_model=NomenclatureResponse)
async def get_nomenclature_by_id(
    nomenclature_id: UUID,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    service = NomenclatureService(db)
    nomenclature = await service.get_by_id(nomenclature_id)
    if not nomenclature:
        raise HTTPException(status_code=404, detail="Nomenclature not found")
    return nomenclature


@router.get("/search/by-name", response_model=NomenclatureListResponse)
async def get_nomenclature_by_name(
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user_from_token)],
    name: str = Query(..., description="Название номенклатуры для поиска")
):
    service = NomenclatureService(db)
    nomenclatures = await service.get_by_name(name)
    return NomenclatureListResponse(nomenclatures=nomenclatures)


@router.post("/", response_model=NomenclatureResponse)
async def create_nomenclature(
    nomenclature_data: NomenclatureCreate,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    service = NomenclatureService(db)
    try:
        nomenclature = await service.create(
            name=nomenclature_data.name,
            description=nomenclature_data.description,
            sku=nomenclature_data.sku,
            type_id=nomenclature_data.type_id,
            group_id=nomenclature_data.group_id,
            measure_unit_id=nomenclature_data.measure_unit_id,
            properties=nomenclature_data.properties
        )
        await db.commit()
        return nomenclature
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{nomenclature_id}", response_model=NomenclatureResponse)
async def update_nomenclature(
    nomenclature_id: UUID,
    nomenclature_data: NomenclatureUpdate,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    service = NomenclatureService(db)
    
    existing_nomenclature = await service.get_by_id(nomenclature_id)
    if not existing_nomenclature:
        raise HTTPException(status_code=404, detail="Nomenclature not found")
    
    try:
        updated_nomenclature = await service.update(
            nomenclature_id=nomenclature_id,
            name=nomenclature_data.name,
            description=nomenclature_data.description,
            sku=nomenclature_data.sku,
            type_id=nomenclature_data.type_id,
            group_id=nomenclature_data.group_id,
            measure_unit_id=nomenclature_data.measure_unit_id,
            properties=nomenclature_data.properties
        )
        await db.commit()
        return updated_nomenclature
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{nomenclature_id}", status_code=200)
async def delete_nomenclature(
    nomenclature_id: UUID,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user_from_token)]
):
    service = NomenclatureService(db)
    
    existing_nomenclature = await service.get_by_id(nomenclature_id)
    if not existing_nomenclature:
        raise HTTPException(status_code=404, detail="Nomenclature not found")
    
    try:
        await service.delete(nomenclature_id)
        await db.commit()
        return {"message": "Nomenclature deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) 
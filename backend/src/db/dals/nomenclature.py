from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models import Nomenclature


class NomenclatureDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> List[Nomenclature]:
        stmt = (
            select(Nomenclature)
            .options(
                joinedload(Nomenclature.type),
                joinedload(Nomenclature.group),
                joinedload(Nomenclature.measure_unit)
            )
            .order_by(Nomenclature.name)
        )
        result = await self.db_session.execute(stmt)
        return list(result.scalars().unique())

    async def get_by_id(self, nomenclature_id: UUID) -> Optional[Nomenclature]:
        stmt = (
            select(Nomenclature)
            .where(Nomenclature.id == nomenclature_id)
            .options(
                joinedload(Nomenclature.type),
                joinedload(Nomenclature.group),
                joinedload(Nomenclature.measure_unit),
                joinedload(Nomenclature.base_recipes),
                joinedload(Nomenclature.recipes)
            )
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_name(self, name: str) -> List[Nomenclature]:
        stmt = (
            select(Nomenclature)
            .where(func.lower(Nomenclature.name).contains(func.lower(name)))
            .options(
                joinedload(Nomenclature.type),
                joinedload(Nomenclature.group),
                joinedload(Nomenclature.measure_unit)
            )
            .order_by(Nomenclature.name)
        )
        result = await self.db_session.execute(stmt)
        return list(result.scalars().unique())
        
    async def create(
        self,
        name: str,
        type_id: UUID,
        group_id: UUID,
        measure_unit_id: UUID,
        description: Optional[str] = None,
        sku: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Nomenclature:
        nomenclature = Nomenclature(
            name=name,
            description=description,
            sku=sku,
            type_id=type_id,
            group_id=group_id,
            measure_unit_id=measure_unit_id,
            properties=properties or {}
        )
        self.db_session.add(nomenclature)
        await self.db_session.flush()
        await self.db_session.refresh(nomenclature)
        return nomenclature
        
    async def update(
        self,
        nomenclature_id: UUID,
        name: str,
        type_id: UUID,
        group_id: UUID,
        measure_unit_id: UUID,
        description: Optional[str] = None,
        sku: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Nomenclature:
        current_properties = {}
        if properties is None:
            nomenclature = await self.get_by_id(nomenclature_id)
            if nomenclature:
                current_properties = nomenclature.properties
        
        stmt = (
            update(Nomenclature)
            .where(Nomenclature.id == nomenclature_id)
            .values(
                name=name,
                description=description,
                sku=sku,
                type_id=type_id,
                group_id=group_id,
                measure_unit_id=measure_unit_id,
                properties=properties or current_properties
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.db_session.execute(stmt)
        
        return await self.get_by_id(nomenclature_id)
        
    async def delete(self, nomenclature_id: UUID) -> None:
        stmt = delete(Nomenclature).where(Nomenclature.id == nomenclature_id)
        await self.db_session.execute(stmt) 
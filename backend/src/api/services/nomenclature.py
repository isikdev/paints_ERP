from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.dals.nomenclature import NomenclatureDAL
from db.models import Nomenclature


class NomenclatureService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.dal = NomenclatureDAL(db_session)

    async def get_all(self) -> List[Nomenclature]:
        return await self.dal.get_all()

    async def get_by_id(self, nomenclature_id: UUID) -> Optional[Nomenclature]:
        return await self.dal.get_by_id(nomenclature_id)
        
    async def get_by_name(self, name: str) -> List[Nomenclature]:
        return await self.dal.get_by_name(name)
        
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
        return await self.dal.create(
            name=name,
            description=description,
            sku=sku,
            type_id=type_id,
            group_id=group_id,
            measure_unit_id=measure_unit_id,
            properties=properties
        )
        
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
        return await self.dal.update(
            nomenclature_id=nomenclature_id,
            name=name,
            description=description,
            sku=sku,
            type_id=type_id,
            group_id=group_id,
            measure_unit_id=measure_unit_id,
            properties=properties
        )
        
    async def delete(self, nomenclature_id: UUID) -> None:
        await self.dal.delete(nomenclature_id) 
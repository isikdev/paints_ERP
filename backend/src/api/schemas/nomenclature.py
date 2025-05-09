from uuid import UUID
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class NomenclatureTypeResponse(BaseModel):
    id: UUID
    name: str


class MeasureUnitResponse(BaseModel):
    id: UUID
    name: str
    short_name: str


class NomenclatureGroupResponse(BaseModel):
    id: UUID
    name: str
    parent_id: Optional[UUID] = None


class NomenclatureResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    type_id: UUID
    group_id: UUID
    measure_unit_id: UUID
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    type: Optional[NomenclatureTypeResponse] = None
    group: Optional[NomenclatureGroupResponse] = None
    measure_unit: Optional[MeasureUnitResponse] = None

    class Config:
        from_attributes = True


class NomenclatureListResponse(BaseModel):
    nomenclatures: List[NomenclatureResponse]


class NomenclatureCreate(BaseModel):
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    type_id: UUID
    group_id: UUID
    measure_unit_id: UUID
    properties: Dict[str, Any] = Field(default_factory=dict)


class NomenclatureUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    type_id: UUID
    group_id: UUID
    measure_unit_id: UUID
    properties: Dict[str, Any] = Field(default_factory=dict) 
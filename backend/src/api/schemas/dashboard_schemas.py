from pydantic import BaseModel, PositiveInt

import datetime
import uuid


class DocumentForDashboard(BaseModel):
    id: uuid.UUID
    document_datetime: datetime.datetime
    counterparty_name: str
    number_of_nomenclatures: PositiveInt


class DashboardResponse(BaseModel):
    operations_today: PositiveInt
    latest_receipts: list[DocumentForDashboard]
    latest_shipments: list[DocumentForDashboard]

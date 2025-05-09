from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
import datetime

from db.engine import get_session
from db.models import Nomenclature, Counterparty, StockMove, Document, DocumentType
from api.schemas import DashboardResponse, DocumentForDashboard

from constants import DocumentTypes, DocumentStatuses

dashboard_router = APIRouter()

@dashboard_router.get("/dashboard")#, response_model=DashboardResponse)
async def get_dashboard_overview(session: AsyncSession = Depends(get_session)):

    today = datetime.date.today()

    operation_types = [dt['name'] for dt in DocumentTypes[2:]]

    operations_today = await session.scalar(
        select(func.count(Document.id)).join(Document.document_type)
        .where(Document.document_datetime == today)
        .where(Document.status == 'Posted')
        .where(DocumentType.name.in_(operation_types))
    )
    return {'ops': operations_today}


    # latest_incoming_query = await session.execute(
    #     select(Receipt.date, Counterparty.name, Receipt.positions_count)
    #     .join(Counterparty, Receipt.counterparty_id == Counterparty.id)
    #     .order_by(desc(Receipt.date))
    #     .limit(3)
    # )
    # latest_incoming = [
    #     StockMove(date=row[0], counterparty=row[1], positions=row[2])
    #     for row in latest_incoming_query.all()
    # ]
    #
    # latest_outgoing_query = await session.execute(
    #     select(Shipment.date, Counterparty.name, Shipment.positions_count)
    #     .join(Counterparty, Shipment.counterparty_id == Counterparty.id)
    #     .order_by(desc(Shipment.date))
    #     .limit(3)
    # )
    # latest_outgoing = [
    #     Entry(date=row[0], counterparty=row[1], positions=row[2])
    #     for row in latest_outgoing_query.all()
    # ]
    #
    # return DashboardOverview(
    #     total_nomenclature=total_nomenclature,
    #     total_counterparties=total_counterparties,
    #     operations_today=operations_today,
    #     production_today=production_today,
    #     latest_incoming=latest_incoming,
    #     latest_outgoing=latest_outgoing,
    # )
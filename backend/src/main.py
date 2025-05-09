from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI

from api.handlers.actions.auth import get_current_user_from_token
from db.models import User
from settings import Settings, get_settings
app = FastAPI(title=get_settings().app_name, version="0.1")
api_router = APIRouter(
    prefix="/api/v1",
    # dependencies = [Depends(get_current_user_from_token)],
)

from api.handlers import base_recipe_router, document_type_router, recipe_router, login_router, dashboard_router, nomenclature_router
api_router.include_router(base_recipe_router)
api_router.include_router(document_type_router)
api_router.include_router(recipe_router)
api_router.include_router(dashboard_router)
api_router.include_router(nomenclature_router)
app.include_router(login_router, prefix="/api/v1")


@api_router.get('/ping')
async def ping(current_user: User = Depends(get_current_user_from_token)):
    """"""
    return {'message': 'Paints ERP backend is running', 'user': current_user}


app.include_router(api_router)

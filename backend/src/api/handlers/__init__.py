from .document_type_handlers import document_type_router
from .base_recipe_handlers import base_recipe_router
from .login_handler import login_router
from .recipe_handlers import recipe_router
from .dashboard_handlers import dashboard_router
from .nomenclature_handlers import router as nomenclature_router

__all__ = (
    'base_recipe_router',
    'document_type_router',
    'login_router',
    'recipe_router',
    'dashboard_router',
    'nomenclature_router',
)

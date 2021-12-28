from fastapi import APIRouter

from app.api.api_v1.endpoints import properties, login, users, property_categories, amenities, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(property_categories.router, prefix="/property_categories", tags=["property categories"])
api_router.include_router(amenities.router, prefix="/amenities", tags=["amenities"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

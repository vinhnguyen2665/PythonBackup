from fastapi import APIRouter

from controller.endpoints import authorization

api_router = APIRouter()
api_router.include_router(authorization.router, tags=["authorization"])

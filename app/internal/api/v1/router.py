from fastapi import APIRouter

from internal.api.v1.application import APPLICATION_ROUTER, CATEGORY_ROUTER

V1_ROUTER = APIRouter(prefix='/v1')
V1_ROUTER.include_router(APPLICATION_ROUTER)
V1_ROUTER.include_router(CATEGORY_ROUTER)

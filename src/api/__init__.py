from fastapi import APIRouter
from api.routes.products import router as products_router

router = APIRouter()
router.include_router(products_router)
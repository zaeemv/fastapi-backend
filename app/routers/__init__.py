from fastapi import APIRouter
from . import customers, auth, users

router = APIRouter()

router.include_router(customers.router)
router.include_router(auth.router)
router.include_router(users.router)


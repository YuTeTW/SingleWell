from fastapi import APIRouter
from . import user, files

router = APIRouter()
router.include_router(user.router, tags=["User"])
router.include_router(files.router, tags=["File"])

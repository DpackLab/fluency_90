from fastapi import APIRouter

from fluency90.api.v1.auth import router as auth_router
from fluency90.api.v1.users import router as users_router

router = APIRouter(prefix="/api/v1")


@router.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "version": "0.1.0"}


# Sub-routers
# Nota: No aplicamos prefix adicional aquí para evitar duplicaciones.
# El contrato final de endpoints se controla en cada router (auth.py, users.py).
router.include_router(auth_router, tags=["auth"])
router.include_router(users_router, tags=["users"])

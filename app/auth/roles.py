# app/auth/roles.py
from typing import Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.token import get_current_user
from app.database import get_db
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol
from app.schemas.usuario_schema import UsuarioTokenData


def require_roles(*nombres: str) -> Callable:
    """
    Devuelve una dependencia que exige que el usuario autenticado
    tenga al menos UNO de los roles indicados en `nombres`.

    Uso:
        @router.post("/algo", dependencies=[Depends(require_roles("admin"))])
        ó
        def endpoint(..., current=Depends(require_roles("admin", "editor"))):
            ...
    """
    if not nombres:
        raise ValueError("Debes indicar al menos un nombre de rol")

    def dependency(
        current: UsuarioTokenData = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> UsuarioTokenData:
        # ¿Existe alguna fila usuario_rol para el usuario actual con rol en `nombres`?
        exists = (
            db.query(UsuarioRol.id)
            .join(Rol, UsuarioRol.rol_id == Rol.id)
            .filter(
                UsuarioRol.usuario_id == current.id,
                Rol.nombre.in_(list(nombres)),
            )
            .first()
        )
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado",
            )
        # Devuelve al usuario (por si el endpoint lo quiere usar)
        return current

    return dependency


# Atajo útil para lo más común:
require_admin = require_roles("admin")

__all__ = ["require_roles", "require_admin"]

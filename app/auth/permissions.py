# app/auth/permissions.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioTokenData
from app.auth.token import get_current_user

from app.models.usuario_rol import UsuarioRol
from app.models.rol import Rol

def require_admin(
    db: Session = Depends(get_db),
    current_user: UsuarioTokenData = Depends(get_current_user),
):
    user_id = current_user.id
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")
    tiene = (
        db.query(UsuarioRol)
        .join(Rol, UsuarioRol.rol_id == Rol.id)
        .filter(UsuarioRol.usuario_id == user_id, Rol.nombre == "admin")
        .first()
    )
    if not tiene:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requiere rol administrador.")
    return True

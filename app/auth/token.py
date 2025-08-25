# app/auth/token.py
from typing import Optional
from datetime import datetime, timedelta
try:
    from datetime import UTC  # py3.11+
except ImportError:
    from datetime import timezone as _timezone
    UTC = _timezone.utc  # type: ignore

from jose import JWTError, jwt
from decouple import config
from app.schemas.usuario_schema import UsuarioTokenData

# Configuración
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30))

# Reforzar claims
ISS = config("JWT_ISS", default="fluency90.api")
AUD = config("JWT_AUD", default="fluency90.front")

def crear_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iss": ISS, "aud": AUD})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str, credentials_exception) -> UsuarioTokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience=AUD, issuer=ISS)
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        return UsuarioTokenData(id=int(sub))
    except JWTError:
        raise credentials_exception

# ----- Seguridad OAuth2 -----
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UsuarioTokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verificar_token(token, credentials_exception)

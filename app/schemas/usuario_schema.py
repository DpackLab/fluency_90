from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    estilo: str | None = None
    nivel_inicial: str | None = None
    idioma_id: int

class UsuarioCreate(UsuarioBase):
    contrasena: str  # solo al crear

class UsuarioResponse(UsuarioBase):
    id: int
    class Config:
        orm_mode = True

class UsuarioTokenData(BaseModel):
    id: int | None = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    contrasena: str

class Token(BaseModel):
    access_token: str
    token_type: str

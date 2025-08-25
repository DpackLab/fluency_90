# from .usuario_schema import UsuarioCreate, UsuarioResponse

# from .contenido_diario import ContenidoDiarioCreate, ContenidoDiarioResponse
# from .registro_sesion import RegistroSesionCreate, RegistroSesionResponse
# from .ejercicio_resuelto import EjercicioResueltoCreate, EjercicioResueltoResponse
# from .tiempo_entrenamiento import TiempoEntrenamientoCreate, TiempoEntrenamientoResponse
# from .rol_schema import RolCreate, RolResponse, UsuarioRolCreate, UsuarioRolResponse
# app/schemas/__init__.py
from .usuario_schema import (
    UsuarioCreate as UsuarioCreate,
    UsuarioResponse as UsuarioResponse,
)
# Descomenta si corresponde y aplica el mismo patrón:
# from .contenido_diario import (
#     ContenidoDiarioCreate as ContenidoDiarioCreate,
#     ContenidoDiarioResponse as ContenidoDiarioResponse,
# )

__all__ = [
    "UsuarioCreate",
    "UsuarioResponse",
    # "ContenidoDiarioCreate",
    # "ContenidoDiarioResponse",
]

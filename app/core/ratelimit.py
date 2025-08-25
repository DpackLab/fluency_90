from decouple import config
from slowapi import Limiter
from slowapi.util import get_remote_address

# Límite por defecto (puedes ajustarlo desde .env -> RATE_LIMIT_DEFAULT="60/minute")
DEFAULT_LIMITS = [config("RATE_LIMIT_DEFAULT", default="60/minute")]

# Limiter global que compartirán la app y las rutas
limiter = Limiter(key_func=get_remote_address, default_limits=DEFAULT_LIMITS)

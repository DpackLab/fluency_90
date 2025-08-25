# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from decouple import config

# Rate limiting (SlowAPI)
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from app.core.ratelimit import limiter  # <— ¡OJO! desde core/ratelimit, no desde rutas

# Rutas del proyecto
from app.routes import (
    usuarios,
    idiomas,
    auth_routes,
    retos,
    contenidos,
    contenidos_diarios,
    registro_sesiones,
    ejercicios_resueltos,
    tiempos_entrenamiento,
    roles,
)

# ---------------- FastAPI ----------------
app = FastAPI(
    title="Fluency 90",
    description="API para la app de entrenamiento de inglés",
    version="0.1.0",
)

# ----------- CORS restringido ------------
raw_origins = config("ALLOW_ORIGINS", default="*")
allow_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins if allow_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Rate limit global (SlowAPI) ----
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# --------------- Routers -----------------
app.include_router(usuarios.router)
app.include_router(idiomas.router)
app.include_router(auth_routes.router)
app.include_router(retos.router)
app.include_router(contenidos.router)
app.include_router(contenidos_diarios.router)
app.include_router(registro_sesiones.router)
app.include_router(ejercicios_resueltos.router)
app.include_router(tiempos_entrenamiento.router)
app.include_router(roles.router)

# --------------- Logging -----------------
logging.basicConfig(level=logging.DEBUG)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fluency90.core.config import settings
from fluency90.api.v1.router import router as api_v1_router

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
)

# CORS básico (abrimos para pruebas locales)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router único v1
app.include_router(api_v1_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

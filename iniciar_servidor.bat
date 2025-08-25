@echo off
cd /d %~dp0
call venv\Scripts\activate
start http://127.0.0.1:8000/docs
echo ===============================
echo Servidor iniciando en: http://127.0.0.1:8000
echo Documentación Swagger: http://127.0.0.1:8000/docs
echo ===============================
uvicorn app.main:app --reload

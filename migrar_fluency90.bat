@echo on
echo =====================================================
echo Migrar Fluency_90 con verificación y parche de env.py
echo =====================================================
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

REM 0) Ir a la carpeta raiz del proyecto
cd /d "%~dp0"
echo [OK] Carpeta actual: %CD%

REM 1) Activar entorno virtual
if not exist "venv\Scripts\activate" (
  echo [ERROR] No se encontro venv\Scripts\activate.
  echo Crea o activa tu entorno primero.
  pause
  exit /b 1
)
call venv\Scripts\activate
echo [OK] Entorno virtual activado.

REM 2) Verificar alembic.ini
if not exist "alembic.ini" (
  echo [ERROR] No se encontro alembic.ini en esta carpeta.
  pause
  exit /b 1
)
echo [OK] alembic.ini encontrado.

REM 3) Parchear alembic/env.py para asegurar import de modelos
echo === Verificando imports en alembic/env.py ===
powershell -Command ^
  "$envPath = 'alembic\\env.py';" ^
  "$content = Get-Content $envPath -Raw;" ^
  "if ($content -notmatch 'from app.models import usuario') {" ^
  "  $importBlock = 'from app.models import (usuario, idioma, contenido, reto, contenido_diario, registro_sesion, ejercicio_resuelto, tiempo_entrenamiento, rol, usuario_rol)';" ^
  "  $content = $content -replace '(?<=from app.database import Base)', 'from app.database import Base`r`n' + $importBlock;" ^
  "  Set-Content $envPath $content;" ^
  "  Write-Host 'Parche aplicado a env.py';" ^
  "} else {Write-Host 'env.py ya contiene import de modelos';}"
echo [OK] Verificación de env.py terminada.

REM 4) Generar migracion con autogenerate y guardar log
set TS=%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set TS=%TS: =0%
set REV_LOG=alembic_gen_%TS%.log
echo === Generando migracion Alembic... ===
alembic revision --autogenerate -m "Auto: nuevos modulos" > "%REV_LOG%" 2>&1
echo [INFO] Log de revision guardado en: %REV_LOG%

REM 4.1) Revisar patrones de error comunes
findstr /i /c:"NoReferencedTableError" /c:"Traceback" /c:"FAILED" /c:"Could not" "%REV_LOG%" >nul
if not errorlevel 1 (
  echo [ERROR] Problemas detectados en la GENERACION de la migracion.
  type "%REV_LOG%"
  pause
  exit /b 1
)
echo [OK] Revision generada sin errores críticos.

REM 5) Aplicar migracion (upgrade head)
set UPG_LOG=alembic_upgrade_%TS%.log
echo === Aplicando migracion... ===
alembic upgrade head > "%UPG_LOG%" 2>&1
echo [INFO] Log de upgrade guardado en: %UPG_LOG%

REM 5.1) Buscar errores en upgrade
findstr /i /c:"Traceback" /c:"FAILED" /c:"ERROR" "%UPG_LOG%" >nul
if not errorlevel 1 (
  echo [ERROR] Problemas detectados en el UPGRADE.
  type "%UPG_LOG%"
  pause
  exit /b 1
)
echo [OK] Migracion aplicada sin errores.

REM 6) Iniciar servidor y Swagger
echo === Iniciando servidor (Uvicorn) ===
start cmd /k "uvicorn app.main:app --reload"
timeout /t 5 >nul
start http://127.0.0.1:8000/docs

echo [OK] Servidor iniciado y Swagger UI abierto.
pause

Fluency_90 – Backend API (FastAPI)

Bienvenido 
Este repositorio contiene el backend de Fluency_90, una plataforma para entrenamiento intensivo de inglés. Está construido con FastAPI + SQLAlchemy, usa JWT para autenticación y persiste datos en PostgreSQL. Incluye migraciones con Alembic, pruebas con pytest y validaciones de seguridad básicas (pre-commit con ruff, bandit y gitleaks).

Objetivo: que cualquier persona (sin experiencia previa) pueda ponerlo a funcionar en su máquina en minutos.

Índice

1. Qué ofrece
2. Arquitectura y tecnologías
3. Estructura del proyecto
4. Requisitos previos
5. Arranque rápido (TL;DR)
6. Configuración detallada
   1) Crear y activar entorno
   2) Instalar dependencias
   3) Configurar variables de entorno
   4) Preparar la base de datos
   5) Ejecutar migraciones
   6) (Opcional) Crear un admin de prueba
   7) Ejecutar el servidor

7. Uso de la API
   - Documentación interactiva
   - Autenticación (JWT)
   -Ejemplo rápido con curl

8. CORS
9. Pruebas y calidad de código
10. CI en GitHub
11. Migraciones: crear nuevas y buenas prácticas
12. Solución de problemas frecuentes
13. Estado y hoja de ruta
14. Licencia y uso

1. Qué ofrece

. API REST para:
    - Usuarios, roles y permisos.
    - Idiomas.
    - Contenidos / contenidos diarios.
    - Registro de sesiones y tiempos de entrenamiento.
    - (Base lista para ejercicios resueltos, retos, etc.)

. Autenticación con JWT (incluye iss y aud).
. Migraciones con Alembic.
. Configuración por .env.
. Documentación OpenAPI/Swagger lista para usar.
. Suite de pruebas inicial con pytest.
. Seguridad básica: CORS configurable, hashing de contraseñas con bcrypt, linters y escáneres de seguridad (pre-commit).

2. Arquitectura y tecnologías

Backend
FastAPI · SQLAlchemy · Alembic · Pydantic

Base de datos
PostgreSQL (local o Docker)

Autenticación
OAuth2 password flow + JWT (python-jose/cryptography, passlib[bcrypt])

Dev & Calidad
pytest · pre-commit (ruff, bandit, gitleaks)

3. Estructura del proyecto
Fluency_90/
├── app/
│   ├── main.py                 # App FastAPI (monta routers, CORS)
│   ├── database.py             # Motor SQLAlchemy y sesión (lee .env)
│   ├── auth/
│   │   ├── token.py            # Crear/verificar JWT, dependencia current_user
│   │   └── roles.py            # Dependencia require_roles (autz)
│   ├── models/                 # Modelos SQLAlchemy
│   ├── schemas/                # Esquemas Pydantic (request/response)
│   └── routes/                 # Endpoints de la API (usuarios, idiomas, etc.)
├── alembic/
│   ├── env.py                  # Config Alembic
│   └── versions/               # Migraciones
├── tests/                      # Pruebas automatizadas (pytest)
├── .github/workflows/ci.yml    # CI (opcional)
├── .pre-commit-config.yaml     # Hooks de calidad/seguridad
├── requirements.txt
├── README.md
└── .env                        # (local, NO subir a Git)

4. Requisitos previos

Python 3.11+

PostgreSQL 13+ (o Docker Desktop si usarás contenedor)

Git (opcional pero recomendado)

Windows: usa PowerShell o CMD.
macOS / Linux: usa Terminal (bash/zsh).

5. Arranque rápido (TL;DR)
# 1) Crear entorno y activarlo
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Crear .env (ver ejemplo más abajo)
# 4) Crear BD (Postgres) y ajustar DATABASE_URL en .env
# 5) Migraciones
alembic upgrade head

# 6) Ejecutar servidor
uvicorn app.main:app --reload
# Abre: http://127.0.0.1:8000/docs


6. Configuración detallada
   1) Crear y activar entorno
      python -m venv venv
      # Windows
      venv\Scripts\activate
      # macOS/Linux
      # source venv/bin/activate

   2) Instalar dependencias
        pip install -r requirements.txt

   3) Configurar variables de entorno
      Crea un archivo .env en la raíz del proyecto con este contenido (ejemplo seguro):
      # Conexión a Postgres (ajusta credenciales/host)
      DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fluency90_db

      # Clave y algoritmo JWT
      SECRET_KEY=CAMBIA_ESTA_CLAVE_POR_UNA_MUY_LARGA_Y_UNICA
      ALGORITHM=HS256
      ACCESS_TOKEN_EXPIRE_MINUTES=30

      # Claims recomendados en JWT
      JWT_ISS=fluency90.api
      JWT_AUD=fluency90.front

      # CORS: orígenes permitidos (separados por coma)
      ALLOW_ORIGINS=http://localhost:5173,https://tu-front.com

      ¿Cómo genero una clave fuerte para SECRET_KEY?

      Windows (PowerShell):
      python - << "PY"
      import secrets; print(secrets.token_urlsafe(64))
      PY

      macOS/Linux:
      python - << 'PY'
      import secrets; print(secrets.token_urlsafe(64))
      PY

      Nunca subas .env a Git.

   4) Preparar la base de datos

      Opción A – local: instala PostgreSQL y crea la DB fluency90_db.
      Opción B – Docker (opcional):
        docker run --name fluency90-db -e POSTGRES_PASSWORD=postgres \
        -e POSTGRES_DB=fluency90_db -p 5432:5432 -d postgres:15

    Ajusta DATABASE_URL a postgresql://postgres:postgres@localhost:5432/fluency90_db.

   5) Ejecutar migraciones
      alembic upgrade head

      Si agregas o cambias modelos: alembic revision --autogenerate -m "mensaje" y luego alembic upgrade head.

   6) (Opcional) Crear un admin de prueba

      Hay un script one-shot (bootstrap_admin.py) para crear idioma base y un usuario admin. Úsalo solo una vez y deshabilítalo después (o bórralo).

      python bootstrap_admin.py
      # Salida esperada:
      # ✅ Listo. Admin creado o verificado:
      #    email:    admin@example.com
      #    password: Admin123!

      Luego no lo vuelvas a ejecutar (o comenta/bórralo) para evitar dejar puertas traseras.

   7) Ejecutar el servidor
      uvicorn app.main:app --reload
      # Abre http://127.0.0.1:8000/docs

7. Uso de la API
   Documentación interactiva

      - Swagger UI: http://127.0.0.1:8000/docs
      - OpenAPI JSON: http://127.0.0.1:8000/openapi.json

   Autenticación (JWT)
   El flujo implementado es OAuth2 password:
      1. Obtén un token con POST /auth/token pasando username (email) y password.
      2. Usa el access_token como Bearer en el header Authorization para acceder a endpoints privados.

   Ejemplo rápido con curl

      # 1) Login
      curl -X POST "http://127.0.0.1:8000/auth/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin@example.com&password=Admin123!"

      # 2) Usar token (reemplaza XXX por el token devuelto)
      curl -H "Authorization: Bearer XXX" \
        "http://127.0.0.1:8000/tiempos-entrenamiento/"

8. CORS

   En app/main.py se activa CORS leyendo ALLOW_ORIGINS del .env.
   Asegúrate de listar solo los dominios de tu frontend. Ejemplos:

   - Desarrollo local:
     ALLOW_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

   - Producción:
     ALLOW_ORIGINS=https://tu-front.com

9. Pruebas y calidad de código

   Ejecutar pruebas
      # (desde la raíz y con el venv activo)
      pytest -q

   Pre-commit (linting & seguridad)
   Este repo usa pre-commit con:

   - ruff (formato y lint),
   - bandit (SAST básico para Python),
   - gitleaks (secrets scan).

   Instalación y primer escaneo:
      pip install pre-commit
      pre-commit install
      python -m pre_commit run --all-files

   Cada git commit ejecutará los hooks automáticamente.

10. CI en GitHub

    Incluimos un workflow opcional .github/workflows/ci.yml que:
    - Arranca un Postgres de prueba,
    - Instala dependencias,
    - Ejecuta migraciones y pytest,
    - Corre ruff/bandit/gitleaks (si los activas en el workflow).

    Para usarlo:
    1. Subí tu repo a GitHub.
    2. Asegúrate de tener el archivo ci.yml.
    3. Crea secrets si luego parametrizas claves (opcional).

11. Migraciones: crear nuevas y buenas prácticas
    1. Modifica/crea modelos en app/models/.
    2. Genera una revisión:
       alembic revision --autogenerate -m "tu mensaje"
    3. Revisa la migración creada en alembic/versions/.
    4. Aplica:
       alembic upgrade head

    Consejos
    - No edites migraciones ya aplicadas en producción.
    - Mantené el archivo alembic/env.py importando Base y cargando todos los modelos (ya está preparado).

12. Solución de problemas frecuentes
    - psycopg2 falla al compilar: usa psycopg2-binary (ya incluido).
    - ModuleNotFoundError: app al correr tests: ejecuta desde la raíz y, si hiciera falta, set PYTHONPATH=. (Windows) o export PYTHONPATH=. (bash).
    - No puedo activar el venv en PowerShell: ejecuta PowerShell como admin y Set-ExecutionPolicy -Scope CurrentUser RemoteSigned.
    - CORS bloquea mi frontend: revisa ALLOW_ORIGINS en .env.
    - 401 al llamar endpoints: verifica que el token esté vigente y envías Authorization: Bearer <token>.

13. Estado y hoja de ruta

    - ✅ Autenticación JWT (con iss/aud)
    - ✅ Módulos base: usuarios, idiomas, contenidos, tiempos
    - ✅ Migraciones + pruebas iniciales
    - 🔜 Endpoints adicionales (más validaciones, reporting, etc.)
    - 🔒 Hardenings extra (rate-limit por IP, rotación de claves, etc.)

14. Licencia y uso

     Proyecto interno de Dpack Software Labs para fines de entrenamiento.
     No distribuible públicamente sin autorización expresa.""    # a�ade una l�nea en blanco, por ejemplo

# Fluency_90 Backend API

Este es el backend desarrollado en **FastAPI** para la aplicación intensiva de entrenamiento de inglés Fluency_90. Está diseñado para manejar usuarios, idiomas, ejercicios, y métricas de progreso, con una arquitectura escalable y moderna.

## 🚀 Tecnologías principales

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn
- Python-dotenv

## 📁 Estructura del proyecto

```
Fluency_90/
├── .env               # Variables de entorno (base de datos, etc.)
├── .gitignore
├── main.py            # Punto de entrada de la API
├── create_db.py       # Creador de tablas iniciales
├── app/
│   ├── database.py
│   ├── models/        # Modelos SQLAlchemy
│   ├── schemas/       # Esquemas Pydantic
│   ├── routes/        # Endpoints de la API
```

## ⚙️ Configuración del entorno

1. Clonar el repositorio.
2. Crear el entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # en Linux/macOS
venv\Scripts\activate     # en Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear archivo `.env`:

```
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fluency90_db
```

5. Ejecutar el servidor:

```bash
uvicorn app.main:app --reload
```

## 📌 Funcionalidades actuales

- Registro y gestión de usuarios
- Registro de idiomas
- Estructura lista para agregar ejercicios, progreso, y sesiones de entrenamiento

## 📄 Licencia

Proyecto interno de entrenamiento creado por **Dpack Software Labs**. No distribuible públicamente sin autorización.

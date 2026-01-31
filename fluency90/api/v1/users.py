from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fluency90.core.database import get_db
from fluency90.core.security import get_current_user, require_admin
from fluency90.services.session_service import get_or_create_active_session

from fluency90.models import User
from fluency90.schemas.user_schema import UserCreate, UserRead
from fluency90.schemas.user_stats_schema import UserMeStats
from fluency90.schemas.output_schema import OutputCreate, OutputRead
from fluency90.schemas.user_schema import UserDailyStateRead

from fluency90.services.output_service import create_user_output
from fluency90.services.user_stats_service import get_user_me_stats
from fluency90.services.event_log_service import log_event
from fluency90.services.user_service import create_user as create_user_service
from fluency90.services.active_day_service import mark_user_active_today

from fluency90.services.progress_policy_service import decision_from_state
from fluency90.services.daily_state_service import get_user_daily_state

from uuid import uuid4

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    # Path canónico (sin slash final)
    path = "/api/v1/users"

    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado",
        )

    user = create_user_service(db=db, user_in=user_in)

    log_event(
        db=db,
        event_type="users_create",
        user_id=None,
        meta={"source": "api", "path": path, "created_email": user.email},
    )

    return user

@router.get("", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    # Path canónico (sin slash final)
    path = "/api/v1/users"

    log_event(
        db=db,
        event_type="users_list_read",
        user_id=current_user.id,
        meta={"source": "api", "path": path},
    )

    users = db.query(User).all()
    return users

@router.get("/me", response_model=UserRead)
def read_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    path = "/api/v1/users/me"

    log_event(
        db=db,
        event_type="users_me_read",
        user_id=current_user.id,
        meta={"source": "api", "path": path},
    )

    return current_user

@router.post("/me/touch", response_model=UserMeStats)
def touch_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Path canónico (sin slash final)
    path = "/api/v1/users/me/touch"

    # 1) Mutación canónica de presencia (único lugar permitido)
    get_or_create_active_session(db, current_user.id)
    mark_user_active_today(db, current_user.id, current_user.timezone)

    # 2) Log gobernado
    log_event(
        db=db,
        event_type="users_me_touch",
        user_id=current_user.id,
        meta={"source": "api", "path": path},
    )

    # 3) Retornar stats (evita doble llamada frontend)
    return get_user_me_stats(db, current_user.id, current_user.timezone)

@router.post("/me/output", response_model=OutputRead)
def users_me_output_create(
    payload_in: OutputCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    rec = create_user_output(
        db=db,
        user_id=current_user.id,
        user_tz=getattr(current_user, "timezone", "UTC"),
        output_type=payload_in.output_type,
        payload=payload_in.payload,
    )

    # CIERRE PASO 2 (DÍA 4): logging "hard" para ver error real si existiera
    log_event(
        db=db,
        event_type="users_me_output_created",
        user_id=current_user.id,
        meta={
            "source": "api",
            "path": "/api/v1/users/me/output",
            "output_id": rec.id,
            "output_type": rec.output_type,
        },
    )

    return rec

@router.get("/me/stats", response_model=UserMeStats)
def read_current_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    path = "/api/v1/users/me/stats"

    log_event(
        db=db,
        event_type="users_me_stats_read",
        user_id=current_user.id,
        meta={"source": "api", "path": path},
    )

    user_tz = getattr(current_user, "timezone", "UTC")
    request_id = str(uuid4())

    # 1) Señales (daily_state)
    state = get_user_daily_state(
        db=db,
        user_id=current_user.id,
        user_tz=user_tz,
    )

    # 2) Política real (decision engine)

    decision = decision_from_state(
        db=db,
        user_id=current_user.id,
        user_tz=user_tz,
        state=state,
        endpoint_path=path,
        request_id=request_id,
    )

    if not decision.allowed:
        try:
            log_event(
                db=db,
                event_type="users_blocked_without_output",
                user_id=current_user.id,
                meta={"source": "api", "path": path, "signals": decision.signals_used},
            )
        except Exception:
            pass

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=decision.reason or "Output requerido para continuar",
        )

    # 3) Stats solo si está permitido
    stats = get_user_me_stats(db, current_user.id, user_tz)
    return stats

@router.get("/me/daily-state", response_model=UserDailyStateRead)
def read_current_user_daily_state(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    path = "/api/v1/users/me/daily-state"

    state = get_user_daily_state(
        db=db,
        user_id=current_user.id,
        user_tz=getattr(current_user, "timezone", "UTC"),
    )

    # Observabilidad mínima: registramos lectura y resultado
    log_event(
        db=db,
        event_type="users_me_daily_state_read",
        user_id=current_user.id,
        meta={
            "source": "api",
            "path": path,
            "date": state.date.isoformat(),
            "active_today": state.active_today,
            "has_output_today": state.has_output_today,
            "blocked_without_output": state.blocked_without_output,
            # derived_state NO se expone al cliente, pero sí sirve para diagnóstico interno:
            "derived_state": state.derived_state,
        },
    )

    # Respuesta pública (sin derived_state)
    return {
        "date": state.date,
        "active_today": state.active_today,
        "has_output_today": state.has_output_today,
        "blocked_without_output": state.blocked_without_output,
        "current_streak": state.current_streak,
        "session_active": state.session_active,
        "session_started_at": state.session_started_at,
    }

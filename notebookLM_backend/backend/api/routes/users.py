from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from backend.db.supabase_client import SupabaseDB
from backend.api.auth import get_current_user, AuthUser

router = APIRouter(prefix="/user", tags=["user"])
db = SupabaseDB()

class UserSessionResponse(BaseModel):
    session_id: str
    user_id: str
    created_at: datetime

def _ensure_profile_row(user: AuthUser) -> None:
    """
    Make sure a matching row exists in public.users for the authenticated Supabase user.
    This avoids FK errors when inserting into sessions (sessions.user_id -> users.id).
    """
    try:
        res = db.select("users", {"id": user.user_id})
        exists = bool(getattr(res, "data", None))
        if not exists:
            # Insert the minimal, schema-safe columns only.
            payload = {
                "id": user.user_id,
                "email": user.email,
                "created_at": datetime.utcnow().isoformat()
            }
            db.insert("users", payload)
    except Exception as e:
        # Surface a clear error if the users table/columns are misconfigured.
        raise HTTPException(status_code=500, detail=f"Failed to ensure profile row: {e}")

@router.post("/session/create", response_model=UserSessionResponse)
def create_session(current: AuthUser = Depends(get_current_user)):
    # Ensure the profile row exists first (id == auth.users.id)
    _ensure_profile_row(current)

    # Create a new session for this user
    session_id = f"sess_{datetime.utcnow().timestamp()}_{current.user_id}"
    created_at = datetime.utcnow()
    try:
        db.insert("sessions", {
            "id": session_id,
            "user_id": current.user_id,
            "created_at": created_at.isoformat()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {e}")

    return UserSessionResponse(session_id=session_id, user_id=current.user_id, created_at=created_at)

@router.get("/session/{session_id}", response_model=UserSessionResponse)
def get_session(session_id: str, current: AuthUser = Depends(get_current_user)):
    res = db.select("sessions", {"id": session_id})
    if not getattr(res, "data", None):
        raise HTTPException(status_code=404, detail="Session not found")
    s = res.data[0]
    if s.get("user_id") != current.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        created = s["created_at"]
        # Handle both naive ISO strings and already-parsed timestamps
        created_dt = created if isinstance(created, datetime) else datetime.fromisoformat(created.replace("Z", "+00:00"))
    except Exception:
        created_dt = datetime.utcnow()  # fallback, shouldn't normally happen
    return UserSessionResponse(
        session_id=s["id"],
        user_id=s["user_id"],
        created_at=created_dt
    )

# (Old /user/token endpoint remains removed)

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

@router.post("/session/create", response_model=UserSessionResponse)
def create_session(current: AuthUser = Depends(get_current_user)):
    session_id = f"sess_{datetime.utcnow().timestamp()}_{current.user_id}"
    created_at = datetime.utcnow()
    db.insert("sessions", {
        "id": session_id,
        "user_id": current.user_id,
        "created_at": created_at.isoformat()
    })
    return UserSessionResponse(session_id=session_id, user_id=current.user_id, created_at=created_at)

@router.get("/session/{session_id}", response_model=UserSessionResponse)
def get_session(session_id: str, current: AuthUser = Depends(get_current_user)):
    res = db.select("sessions", {"id": session_id})
    if not res.data:
        raise HTTPException(status_code=404, detail="Session not found")
    s = res.data[0]
    if s.get("user_id") != current.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return UserSessionResponse(
        session_id=s["id"],
        user_id=s["user_id"],
        created_at=datetime.fromisoformat(s["created_at"])
    )

# Remove the old /user/token endpoint entirely.

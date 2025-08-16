"""
API routes for user and session management.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from backend.config import JWT_SECRET_KEY
from backend.db.supabase_client import SupabaseDB

router = APIRouter(prefix="/user", tags=["user"])

db = SupabaseDB()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserSessionCreateRequest(BaseModel):
    user_id: str
    # Optionally, add more fields (e.g., device info)

class UserSessionResponse(BaseModel):
    session_id: str
    user_id: str
    created_at: datetime

# JWT utility functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Dependency for protected routes
def get_current_user(token: str = Depends(lambda: None)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    return verify_token(token)

@router.post("/session/create", response_model=UserSessionResponse)
def create_session(req: UserSessionCreateRequest):
    """Create a new user session and return session info."""
    session_id = f"sess_{datetime.utcnow().timestamp()}_{req.user_id}"
    created_at = datetime.utcnow()
    db.insert("sessions", {"id": session_id, "user_id": req.user_id, "created_at": created_at.isoformat()})
    return UserSessionResponse(session_id=session_id, user_id=req.user_id, created_at=created_at)

@router.get("/session/{session_id}", response_model=UserSessionResponse)
def get_session(session_id: str):
    """Retrieve session info by session_id."""
    res = db.select("sessions", {"id": session_id})
    if not res.data or len(res.data) == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    s = res.data[0]
    return UserSessionResponse(session_id=s["id"], user_id=s["user_id"], created_at=datetime.fromisoformat(s["created_at"]))

class TokenRequest(BaseModel):
    user_id: str

@router.post("/token", response_model=Token)
def issue_token(req: TokenRequest):
    """Issue a JWT token for a user (for demo; in production, add password auth)."""
    access_token = create_access_token({"sub": req.user_id})
    return Token(access_token=access_token)

from dataclasses import dataclass
from fastapi import HTTPException, Request
from jose import jwt, JWTError
from backend.config import SUPABASE_JWT_SECRET, SUPABASE_ISSUER, SUPABASE_AUDIENCE

@dataclass
class AuthUser:
    user_id: str
    email: str | None = None

async def get_current_user(request: Request) -> AuthUser:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = auth.split(" ", 1)[1].strip()

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,   # HS256 shared secret
            algorithms=["HS256"],
            audience=SUPABASE_AUDIENCE,
            issuer=SUPABASE_ISSUER,
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Token missing subject")
    return AuthUser(user_id=sub, email=payload.get("email"))

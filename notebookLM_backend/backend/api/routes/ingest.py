from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
from datetime import datetime
import tempfile, shutil, os
from backend.db.supabase_client import SupabaseDB
from backend.api.auth import get_current_user, AuthUser

router = APIRouter(prefix="/ingest", tags=["ingest"])
db = SupabaseDB()

@router.post("/upload")
async def upload_book(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: Optional[str] = Form(None),
    genre: str = Form(...),
    current: AuthUser = Depends(get_current_user),
):
    try:
        suffix = os.path.splitext(file.filename or "")[1] or ".bin"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            await file.seek(0)
            shutil.copyfileobj(file.file, tmp)

        created_at = datetime.utcnow().isoformat()
        book = {
            "id": f"book_{int(datetime.utcnow().timestamp()*1000)}",
            "title": title,
            "author": author,
            "genre": genre,
            "file_url": tmp_path,  # later: move to storage
            "created_at": created_at
        }
        db.insert("books", book)
        return {"ok": True, "book": book}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {e}")

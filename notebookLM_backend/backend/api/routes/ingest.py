"""
API route for document ingestion and chunk upload.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.db.supabase_client import SupabaseDB
from ingest.document_processor import DocumentProcessor
import os
import shutil

router = APIRouter(prefix="/ingest", tags=["ingest"])

db = SupabaseDB()
processor = DocumentProcessor()

class IngestResponse(BaseModel):
    book_id: str
    num_chunks: int
    message: str

@router.post("/upload", response_model=IngestResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: Optional[str] = Form(None),
    genre: str = Form(...)
):
    """Upload a PDF, process it, and store book/chunks in Supabase."""
    try:
        # Save uploaded file to temp location
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Insert book metadata
        book_id = str(os.urandom(8).hex())
        db.insert("books", {
            "id": book_id,
            "title": title,
            "author": author,
            "genre": genre,
            "file_url": temp_path
        })
        # Process document
        chunks = processor.process_document(temp_path)
        chunks = processor.generate_embeddings(chunks)
        ready_chunks = processor.prepare_chunks_for_db(chunks, book_id, genre)
        # Upload chunks
        for chunk in ready_chunks:
            db.insert("document_chunks", chunk)
        # Clean up temp file
        os.remove(temp_path)
        return IngestResponse(book_id=book_id, num_chunks=len(ready_chunks), message="Document processed and uploaded successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {e}")

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import users, chatbot, mcq, ocr, books, ingest
from backend.api.auth import get_current_user  # NEW

app = FastAPI(title="NotebookLM Backend", version="0.1.0")

# CORS (set your frontend origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protect all “app” routers by default (leave root public)
app.include_router(users.router, dependencies=[Depends(get_current_user)])
app.include_router(chatbot.router, dependencies=[Depends(get_current_user)])
app.include_router(mcq.router, dependencies=[Depends(get_current_user)])
app.include_router(ocr.router, dependencies=[Depends(get_current_user)])
app.include_router(books.router, dependencies=[Depends(get_current_user)])
app.include_router(ingest.router, dependencies=[Depends(get_current_user)])

@app.get("/")
def root():
    return {"message": "NotebookLM Backend is vibing!"}

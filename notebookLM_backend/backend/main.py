from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from backend.api.routes import users, chatbot, mcq, ocr, books, ingest

app = FastAPI(title="NotebookLM Backend", version="0.1.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(users.router)
app.include_router(chatbot.router)
app.include_router(mcq.router)
app.include_router(ocr.router)
app.include_router(books.router)
app.include_router(ingest.router)

@app.get("/")
def root():
    return {"message": "NotebookLM Backend is vibing!"}

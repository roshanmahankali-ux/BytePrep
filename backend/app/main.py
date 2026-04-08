from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.flashcardAPIs import router as flashcard_router

app = FastAPI(title="Flashcard API")

# adding CORS to allow cross port requests - react(port 5173) and FastAPI (port 8000) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flashcard_router, prefix="/api/flashcards", tags=["Flashcards"])

@app.get("/")
async def root():
    return {"message": "Flashcard API is running"}
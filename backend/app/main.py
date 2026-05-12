from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.flashcardAPIs import router as flashcard_router
from app.routes.authRoutes import router as auth_router
from app.routes.adminRoutes import router as admin_router

app = FastAPI(title="Flashcard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flashcard_router, prefix="/api/flashcards", tags=["Flashcards"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Flashcard API is running"}
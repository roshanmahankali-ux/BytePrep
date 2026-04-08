from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class FlashcardCreate(BaseModel):
    question: str
    answer: str
    category: str
    difficulty: str  # "Easy" | "Medium" | "Hard",
    favourite: bool = False

class FlashcardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    favourite: Optional[bool] = None

class FlashcardResponse(BaseModel):
    id: str
    question: str
    answer: str
    category: str
    difficulty: str
    flipped: bool
    favourite: bool


    class Config:
        populate_by_name = True
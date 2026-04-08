from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.flashcard_DataModel import FlashcardCreate, FlashcardUpdate, FlashcardResponse
from bson import ObjectId

router = APIRouter()

def format_card(card) -> dict:
    """Converting MongoDB data to clean response format json objects"""
    return {
        "id": str(card["_id"]),
        "question": card["question"],
        "answer": card["answer"],
        "category": card["category"],
        "difficulty": card["difficulty"],
        "flipped": card.get("flipped", False),
        "favourite": card.get("favourite", False)
    }

# READ — this is to support filtering by difficulty level  AND/OR Favourite for the questions 
@router.get("/", response_model=list[FlashcardResponse])
async def get_flashcards(difficulty: str = None, favourite: bool = None):
    query = {}
    if difficulty:
        query["difficulty"] = difficulty
    if favourite is not None:
        query["favourite"] = favourite
    cards = await db.flashcards.find(query).to_list(1000)
    return [format_card(c) for c in cards]

# READ — this is to get single flashcard by id
@router.get("/{card_id}", response_model=FlashcardResponse)
async def get_flashcard(card_id: str):
    card = await db.flashcards.find_one({"_id": ObjectId(card_id)})
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return format_card(card)

# CREATE — this is to add a new flashcard
@router.post("/", response_model=FlashcardResponse, status_code=201)
async def create_flashcard(data: FlashcardCreate):
    new_card = data.dict()
    new_card["flipped"] = False
    result = await db.flashcards.insert_one(new_card)
    created = await db.flashcards.find_one({"_id": result.inserted_id})
    return format_card(created)

# UPDATE — this is to edit an existing flashcard
@router.put("/{card_id}", response_model=FlashcardResponse)
async def update_flashcard(card_id: str, data: FlashcardUpdate):
    updates = {k: v for k, v in data.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    await db.flashcards.update_one(
        {"_id": ObjectId(card_id)},
        {"$set": updates}
    )
    updated = await db.flashcards.find_one({"_id": ObjectId(card_id)})
    if not updated:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return format_card(updated)

# DELETE — this is to remove a flashcard, returns 204 on success
@router.delete("/{card_id}")
async def delete_flashcard(card_id: str):
    result = await db.flashcards.delete_one({"_id": ObjectId(card_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Flashcard not found")
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import db
from app.auth import get_current_user, get_admin_user
from bson import ObjectId
from datetime import datetime

router = APIRouter()


def format_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "is_admin": user.get("is_admin", False)
    }


def format_history(entry) -> dict:
    return {
        "id": str(entry["_id"]),
        "user_id": str(entry["user_id"]),
        "card_id": str(entry["card_id"]),
        "question": entry.get("question", ""),
        "difficulty": entry.get("difficulty", ""),
        "category": entry.get("category", ""),
        "reviewed_at": entry["reviewed_at"].isoformat()
    }


# ── GET ALL USERS ─────────────────────────────────────────
@router.get("/users")
async def get_all_users(admin=Depends(get_admin_user)):
    """
    Admin only — returns list of all registered users.
    get_admin_user dependency automatically rejects non-admins with 403.
    """
    users = await db.users.find().to_list(1000)
    return [format_user(u) for u in users]


# ── GET USER HISTORY ──────────────────────────────────────
@router.get("/users/{user_id}/history")
async def get_user_history(user_id: str, admin=Depends(get_admin_user)):
    """
    Admin only — returns full review history for a specific user.
    Shows which cards they reviewed, when, and at what difficulty.
    """
    # Verify user exists first
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    history = await db.history.find(
        {"user_id": ObjectId(user_id)}
    ).sort("reviewed_at", -1).to_list(1000)

    return {
        "user": format_user(user),
        "total_reviewed": len(history),
        "history": [format_history(h) for h in history]
    }


# ── GET ALL HISTORY ───────────────────────────────────────
@router.get("/history")
async def get_all_history(admin=Depends(get_admin_user)):
    """
    Admin only — returns review history across all users.
    Useful for seeing overall app usage.
    """
    history = await db.history.find().sort(
        "reviewed_at", -1
    ).to_list(1000)
    return [format_history(h) for h in history]


# ── DELETE USER ───────────────────────────────────────────
@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str, admin=Depends(get_admin_user)):
    """
    Admin only — delete a user and their entire history.
    """
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    # Also clean up their history
    await db.history.delete_many({"user_id": ObjectId(user_id)})


# ── DELETE USER HISTORY ───────────────────────────────────
@router.delete("/users/{user_id}/history", status_code=204)
async def clear_user_history(user_id: str, admin=Depends(get_admin_user)):
    """
    Admin only — clear a user's review history without deleting the account.
    """
    await db.history.delete_many({"user_id": ObjectId(user_id)})


# ── UPDATE USER (make admin / demote) ─────────────────────
@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    data: dict,
    admin=Depends(get_admin_user)
):
    """
    Admin only — update a user's details.
    Main use case: promote/demote admin status.
    """
    allowed_fields = {"username", "is_admin"}
    updates = {k: v for k, v in data.items() if k in allowed_fields}

    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updates}
    )
    updated = await db.users.find_one({"_id": ObjectId(user_id)})
    return format_user(updated)
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.database import db
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from bson import ObjectId

router = APIRouter()


def format_user(user) -> dict:
    """Convert MongoDB user document to clean response format"""
    user_id = user.get("_id") or user.get("id")
    return {
        "id": str(user_id),
        "username": user["username"],
        "email": user["email"],
        "is_admin": user.get("is_admin", False)
    }


# ── REGISTER ──────────────────────────────────────────────
@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: UserRegister):
    """
    Create a new user account.
    1. Check email isn't already taken
    2. Hash the password
    3. Save to DB
    4. Return a JWT token immediately (so user is logged in right after signup)
    """

    # Check if email already exists
    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )

    # Check if username already exists
    existing_username = await db.users.find_one({"username": data.username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken"
        )

    # Hash password — never store plain text
    new_user = {
        "username": data.username,
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "is_admin": data.is_admin
    }

    result = await db.users.insert_one(new_user)
    created = await db.users.find_one({"_id": result.inserted_id})

    # Create JWT token with user ID and admin status
    token = create_access_token({
        "sub": str(created["_id"]),
        "is_admin": created.get("is_admin", False)
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": format_user(created)
    }


# ── LOGIN ─────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """
    Log in with email + password.
    1. Find user by email
    2. Verify password against stored hash
    3. Return JWT token
    """

    # Find user by email
    user = await db.users.find_one({"email": data.email})

    # Intentionally vague error to avoid any SQL injection related Data pharming
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = create_access_token({
        "sub": str(user["_id"]),
        "is_admin": user.get("is_admin", False)
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": format_user(user)
    }


# ── ME ────────────────────────────────────────────────────
@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    """
    Returns the currently logged in user's info.
    Frontend calls this on page load to check if token is still valid.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not logged in")
    return format_user(current_user)

# ── UPDATE OWN PROFILE ────────────────────────────────────
@router.put("/me", response_model=UserResponse)
async def update_me(
    data: dict,
    current_user=Depends(get_current_user)
):
    """User can update their own username or password"""
    allowed = {"username", "password"}
    updates = {k: v for k, v in data.items() if k in allowed}

    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    # Hash password if being updated
    if "password" in updates:
        updates["hashed_password"] = hash_password(updates.pop("password"))

    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": updates}
    )
    updated = await db.users.find_one({"_id": current_user["_id"]})
    return format_user(updated)


# ── DELETE OWN ACCOUNT ────────────────────────────────────
@router.delete("/me", status_code=204)
async def delete_me(current_user=Depends(get_current_user)):
    """User can delete their own account + their history"""
    await db.users.delete_one({"_id": current_user["_id"]})
    await db.history.delete_many({"user_id": current_user["_id"]})


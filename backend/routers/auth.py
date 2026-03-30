from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.database import db
from core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])

# ================= SCHEMA =================
class LoginRequest(BaseModel):
    username: str
    password: str


# ================= LOGIN =================
@router.post("/login")
def login(data: LoginRequest):
    # 🔍 Find user in DB
    row = db.run_one(
        "MATCH (u:User {username:$u}) RETURN u",
        u=data.username
    )

    if not row:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user = row["u"]

    # 🔐 Check password
    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 🔑 Create tokens
    payload = {
        "sub": user["username"],
        "role": user["role"]
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    # ✅ RETURN FORMAT (VERY IMPORTANT FOR FRONTEND)
    return {
        "success": True,
        "data": {
            "token": access_token,
            "refresh_token": refresh_token,
            "username": user["username"],
            "role": user["role"],
            "fullName": user.get("username")
        }
    }


# ================= REFRESH =================
@router.post("/refresh")
def refresh(data: dict):
    payload = verify_token(data.get("refresh_token"))

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_access_token({
        "sub": payload["sub"],
        "role": payload["role"]
    })

    return {
        "success": True,
        "access_token": new_access
    }

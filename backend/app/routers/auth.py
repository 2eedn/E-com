from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.hash import bcrypt
import jwt, os
from ..db import get_db
from ..models import User

from pydantic import BaseModel, EmailStr

class LoginIn(BaseModel):
    email: EmailStr
    password: str

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == payload.email))).scalars().first()
    if not user or not user.password_hash or not bcrypt.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"sub": str(user.id)}, os.getenv("JWT_SECRET", "changeme"), algorithm="HS256")
    return {"token": token}

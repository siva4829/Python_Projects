from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from database import get_db
from model import User
from schemas import CreateUser,Login_User
from auth import hashed_password,check_password,create_access_token

router = APIRouter()

@router.post("/register")
async def  register(user: CreateUser, db: AsyncSession = Depends(get_db)):
    result = await  db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"User {user.username} already exists"
        )
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password(user.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {
        "message": "User created successfully"
    }


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            User.username == form_data.username
        )
    )

    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not check_password(
        form_data.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {"sub": existing_user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

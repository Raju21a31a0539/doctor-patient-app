from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=201
)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(
        models.User
    ).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = models.User(
        username=user.username,
        hashed_password=hash_password(
            user.password
        )
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }
@router.post(
    "/login",
    response_model=schemas.TokenResponse
)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = db.query(
        models.User
    ).filter(
        models.User.username == user.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token({
        "sub": existing_user.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
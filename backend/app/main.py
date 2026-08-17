from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import jwt, JWTError

from .database import Base, engine, get_db
from .models import User, Food
from .schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    FoodCreate,
    FoodResponse,
)
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NutriTrack API",
    description="API do projeto NutriTrack — AC1",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = int(payload["sub"])

    except (JWTError, ValueError, KeyError):
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
        )

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado",
        )

    return user


@app.get("/")
def root():
    return {
        "message": "NutriTrack API funcionando",
        "version": "1.0.0",
    }


@app.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="E-mail já cadastrado",
        )

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post(
    "/auth/login",
    response_model=TokenResponse,
)
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if not user or not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
        )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


@app.get(
    "/auth/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@app.post(
    "/foods",
    response_model=FoodResponse,
    status_code=201,
)
def create_food(
    data: FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    food = Food(**data.model_dump())

    db.add(food)
    db.commit()
    db.refresh(food)

    return food


@app.get(
    "/foods",
    response_model=list[FoodResponse],
)
def list_foods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.scalars(
        select(Food).order_by(Food.name)
    ).all()

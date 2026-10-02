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
    description="API do projeto NutriTrack — AC2",
    version="2.0.0",
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
        "version": "2.0.0",
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

# AC2 — CRUD de refeições, sempre limitado ao usuário autenticado.
from datetime import date
from fastapi import Response
from .models import Meal, MealItem
from .schemas import MealCreate, MealResponse


def validated_items(data: MealCreate, db: Session):
    ids = [item.food_id for item in data.items]
    found = set(db.scalars(select(Food.id).where(Food.id.in_(ids))).all())
    if set(ids) != found:
        raise HTTPException(status_code=422, detail="Um dos alimentos não existe no catálogo.")
    return [MealItem(**item.model_dump()) for item in data.items]


def owned_meal(meal_id: int, user: User, db: Session):
    meal = db.scalar(select(Meal).where(Meal.id == meal_id, Meal.user_id == user.id))
    if meal is None:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    return meal


@app.post("/meals", response_model=MealResponse, status_code=201)
def create_meal(data: MealCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    items = validated_items(data, db)
    meal = Meal(user_id=current_user.id, **data.model_dump(exclude={"items"}), items=items)
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal


@app.get("/meals", response_model=list[MealResponse])
def list_meals(date: date, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return db.scalars(select(Meal).where(Meal.user_id == current_user.id, Meal.date == date)
                      .order_by(Meal.id)).all()


@app.put("/meals/{meal_id}", response_model=MealResponse)
def update_meal(meal_id: int, data: MealCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    meal = owned_meal(meal_id, current_user, db)
    items = validated_items(data, db)
    meal.date, meal.meal_type, meal.notes = data.date, data.meal_type, data.notes
    meal.items = items
    db.commit()
    db.refresh(meal)
    return meal


@app.delete("/meals/{meal_id}", status_code=204)
def delete_meal(meal_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db.delete(owned_meal(meal_id, current_user, db))
    db.commit()
    return Response(status_code=204)

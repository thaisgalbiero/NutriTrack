from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class FoodCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    calories: float = Field(ge=0)
    protein: float = Field(ge=0)
    carbs: float = Field(ge=0)
    fat: float = Field(ge=0)

class FoodResponse(FoodCreate):
    id: int

    class Config:
        from_attributes = True

from datetime import date
from typing import Literal
from pydantic import field_validator

class MealItemCreate(BaseModel):
    food_id: int = Field(gt=0)
    quantity_g: float = Field(gt=0, le=10000, allow_inf_nan=False)

class MealCreate(BaseModel):
    date: date
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"]
    notes: str = Field(default="", max_length=500)
    items: list[MealItemCreate] = Field(min_length=1, max_length=50)

    @field_validator("items")
    @classmethod
    def unique_foods(cls, items):
        if len({item.food_id for item in items}) != len(items):
            raise ValueError("Informe cada alimento uma vez e ajuste sua quantidade.")
        return items

class MealItemResponse(BaseModel):
    id: int
    food_id: int
    quantity_g: float
    food: FoodResponse
    model_config = {"from_attributes": True}

class MealResponse(BaseModel):
    id: int
    date: date
    meal_type: str
    notes: str
    items: list[MealItemResponse]
    model_config = {"from_attributes": True}

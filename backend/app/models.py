from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    calories: Mapped[float] = mapped_column(Float)
    protein: Mapped[float] = mapped_column(Float)
    carbs: Mapped[float] = mapped_column(Float)
    fat: Mapped[float] = mapped_column(Float)

# AC2: as refeições pertencem ao usuário; o catálogo de alimentos é compartilhado.
from datetime import date
from sqlalchemy import Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class Meal(Base):
    __tablename__ = "meals"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    meal_type: Mapped[str] = mapped_column(String(20))
    notes: Mapped[str] = mapped_column(String(500), default="")
    items: Mapped[list["MealItem"]] = relationship(cascade="all, delete-orphan", lazy="selectin")
    __table_args__ = (CheckConstraint("meal_type IN ('breakfast','lunch','dinner','snack')"),)

class MealItem(Base):
    __tablename__ = "meal_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), index=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    quantity_g: Mapped[float] = mapped_column(Float)
    food: Mapped["Food"] = relationship(lazy="joined")
    __table_args__ = (CheckConstraint("quantity_g > 0 AND quantity_g <= 10000"),)

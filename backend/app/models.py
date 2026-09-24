from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Restaurant(Base):
    __tablename__ = "restaurant"

    restaurant_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    restaurant_type: Mapped[str] = mapped_column(String(100), nullable=False)
    cuisine_type: Mapped[str] = mapped_column(String(100), nullable=False)
    average_rating: Mapped[Decimal | None] = mapped_column(Numeric(2, 1), nullable=True)

    reviews: Mapped[list["Review"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "review"

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.restaurant_id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    restaurant: Mapped[Restaurant] = relationship(back_populates="reviews")

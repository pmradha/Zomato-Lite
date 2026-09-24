from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    review_text: str = Field(min_length=1, max_length=2000)


class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    review_text: str | None = Field(default=None, min_length=1, max_length=2000)


class ReviewResponse(BaseModel):
    review_id: int
    rating: int
    review_text: str
    created_at: datetime


class RatingResponse(BaseModel):
    restaurant_name: str
    average_rating: Decimal | None
    review_count: int

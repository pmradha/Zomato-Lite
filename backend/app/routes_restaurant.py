from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import get_db
from .models import Review
from .schemas import RatingResponse
from .services import get_restaurant

router = APIRouter(prefix="/restaurant", tags=["restaurant"])


@router.get("/rating", response_model=RatingResponse)
def get_rating(db: Session = Depends(get_db)) -> RatingResponse:
    restaurant = get_restaurant(db)
    review_count = db.scalar(
        select(func.count(Review.review_id)).where(Review.restaurant_id == restaurant.restaurant_id)
    ) or 0
    return RatingResponse(
        restaurant_name=restaurant.name,
        average_rating=restaurant.average_rating,
        review_count=review_count,
    )

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import Review
from .schemas import ReviewCreate, ReviewResponse, ReviewUpdate
from .services import get_restaurant, refresh_average_rating

router = APIRouter(prefix="/reviews", tags=["reviews"])


def to_response(review: Review) -> ReviewResponse:
    return ReviewResponse(
        review_id=review.id,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at,
    )


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)) -> ReviewResponse:
    restaurant = get_restaurant(db)
    review = Review(restaurant_id=restaurant.id, rating=payload.rating, comment=payload.comment)
    db.add(review)
    db.flush()
    refresh_average_rating(db, restaurant)
    db.commit()
    db.refresh(review)
    return to_response(review)


@router.get("", response_model=list[ReviewResponse])
def list_reviews(db: Session = Depends(get_db)) -> list[ReviewResponse]:
    restaurant = get_restaurant(db)
    reviews = db.scalars(
        select(Review).where(Review.restaurant_id == restaurant.id).order_by(Review.created_at.desc())
    ).all()
    return [to_response(review) for review in reviews]


@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: UUID, payload: ReviewUpdate, db: Session = Depends(get_db)) -> ReviewResponse:
    review = db.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="At least one review field is required")
    for field, value in changes.items():
        setattr(review, field, value)
    restaurant = get_restaurant(db)
    db.flush()
    refresh_average_rating(db, restaurant)
    db.commit()
    db.refresh(review)
    return to_response(review)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: UUID, db: Session = Depends(get_db)) -> Response:
    review = db.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    restaurant = get_restaurant(db)
    db.delete(review)
    db.flush()
    refresh_average_rating(db, restaurant)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

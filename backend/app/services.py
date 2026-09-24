from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Restaurant, Review

RESTAURANT_ID = 1


def refresh_average_rating(session: Session, restaurant: Restaurant) -> None:
    average = session.scalar(
        select(func.avg(Review.rating)).where(Review.restaurant_id == restaurant.restaurant_id)
    )
    restaurant.average_rating = Decimal(str(average)).quantize(Decimal("0.1")) if average is not None else None


def get_restaurant(session: Session) -> Restaurant:
    restaurant = session.get(Restaurant, RESTAURANT_ID)
    if restaurant is None:
        raise LookupError("The configured restaurant has not been initialized")
    return restaurant

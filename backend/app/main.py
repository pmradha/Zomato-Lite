from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal
from .models import Restaurant
from .routes_restaurant import router as restaurant_router
from .routes_reviews import router as reviews_router

app = FastAPI(title="Zomato-Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def initialize_database() -> None:
    with SessionLocal() as session:
        if session.get(Restaurant, 1) is None:
            session.add(
                Restaurant(
                    id=1,
                    name="Ludhiana Burrito",
                    location="Sector 32",
                    restaurant_type="Dine-in",
                    cuisine="Indian",
                    average_rating=None,
                )
            )
            session.commit()


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(reviews_router)
app.include_router(restaurant_router)

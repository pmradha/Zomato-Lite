CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    location VARCHAR(120) NOT NULL,
    restaurant_type VARCHAR(40) NOT NULL,
    cuisine VARCHAR(80) NOT NULL,
    average_rating NUMERIC(3, 2)
);

CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO restaurants (id, name, location, restaurant_type, cuisine, average_rating)
VALUES (1, 'Ludhiana Burrito', 'Sector 32', 'Dine-in', 'Indian', NULL);

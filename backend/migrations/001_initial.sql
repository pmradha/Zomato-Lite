-- This migration documents the authoritative V1 schema used by Neon.
-- It is non-destructive and does not alter an existing matching schema.
CREATE TABLE IF NOT EXISTS restaurant (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    restaurant_type VARCHAR(100) NOT NULL,
    cuisine_type VARCHAR(100) NOT NULL,
    average_rating NUMERIC(2, 1)
);

CREATE TABLE IF NOT EXISTS review (
    review_id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL REFERENCES restaurant(restaurant_id),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO restaurant (restaurant_id, name, location, restaurant_type, cuisine_type, average_rating)
VALUES (1, 'Ludhiana Burrito', 'Sector 32', 'Dine-in', 'Indian', NULL)
ON CONFLICT (restaurant_id) DO NOTHING;

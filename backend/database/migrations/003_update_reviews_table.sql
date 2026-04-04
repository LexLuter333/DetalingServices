-- Migration 003: Update reviews table schema
-- This migration recreates the reviews table with new structure

-- Drop existing tables (if they exist)
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS review_sources;

-- Create new reviews table with simplified structure
CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,           -- Имя клиента
    car_brand TEXT NOT NULL,      -- Марка автомобиля
    car_model TEXT NOT NULL,      -- Модель автомобиля
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    text TEXT NOT NULL,           -- Текст отзыва
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for sorting by creation date
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at DESC);

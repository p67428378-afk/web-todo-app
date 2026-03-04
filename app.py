"""
Module: app
Purpose: Flask application for the Wishlist Service.
Author: Developer_Agent
Created: 2026-03-04
Notes: Implements core wishlist functionalities as per HLD SCRUM-10.
"""

import os
import uuid
import json
from datetime import datetime

import psycopg2
import redis
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/wishlist_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Connect to PostgreSQL
def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Connect to Redis
def get_redis_connection():
    """Establishes and returns a connection to the Redis cache."""
    r = redis.from_url(REDIS_URL)
    return r

# Initialize database schema (for demonstration purposes)
def init_db():
    """Initializes the database schema if tables do not exist."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS wishlists (
                wishlist_id UUID PRIMARY KEY,
                user_id UUID NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS wishlist_items (
                item_id UUID PRIMARY KEY,
                wishlist_id UUID NOT NULL REFERENCES wishlists(wishlist_id) ON DELETE CASCADE,
                product_id VARCHAR(255) NOT NULL,
                quantity INTEGER DEFAULT 1,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'active',
                CONSTRAINT unique_wishlist_product UNIQUE (wishlist_id, product_id)
            );
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        app.logger.error(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

# Placeholder for external service interactions
def get_product_details(product_id: str) -> dict:
    """
    Simulates fetching product details from a Product Catalog Service.
    In a real application, this would be an HTTP call to another microservice.
    """
    # Mock data for demonstration
    mock_products = {
        "prod123": {"name": "Laptop Pro", "price": 1200.00, "in_stock": True},
        "prod456": {"name": "Mechanical Keyboard", "price": 150.00, "in_stock": True},
        "prod789": {"name": "Monitor Ultra", "price": 450.00, "in_stock": False},
    }
    return mock_products.get(product_id, None)

def validate_user(user_id: str) -> bool:
    """
    Simulates validating a user with the User Service.
    In a real application, this would be an HTTP call to another microservice.
    """
    # Mock validation: assume any non-empty user_id is valid
    return bool(user_id)

def add_to_shopping_cart(user_id: str, product_id: str, quantity: int) -> bool:
    """
    Simulates adding a product to the shopping cart via the Shopping Cart Service.
    In a real application, this would be an HTTP call to another microservice.
    """
    app.logger.info(f"Simulating adding product {product_id} (qty: {quantity}) to user {user_id}'s cart.")
    return True # Assume success for simulation

def send_share_notification(user_id: str, share_link: str, recipient_emails: list = None) -> bool:
    """
    Simulates sending a share notification via the Notification Service.
    In a real application, this would be an HTTP call to another microservice.
    """
    app.logger.info(f"Simulating sharing wishlist for user {user_id} via link: {share_link} to {recipient_emails}")
    return True # Assume success for simulation

@app.before_request
def before_request_func():
    """Ensure database is initialized before the first request."""
    if not hasattr(app, 'database_initialized'):
        init_db()
        app.database_initialized = True

@app.route("/")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "Wishlist Service is up and running!"}), 200

# API Endpoints will be added here

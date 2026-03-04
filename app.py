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


# API Endpoints

@app.route("/wishlist/<uuid:user_id>", methods=["POST"])
def create_or_get_wishlist(user_id):
    """Creates a new wishlist for a user or retrieves an existing one."""
    if not validate_user(str(user_id)):
        return jsonify({"message": "Invalid user ID"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Try to find an existing wishlist
        cur.execute("SELECT wishlist_id FROM wishlists WHERE user_id = %s", (str(user_id),))
        wishlist = cur.fetchone()

        if wishlist:
            wishlist_id = wishlist[0]
            return jsonify({"message": "Wishlist already exists", "wishlist_id": wishlist_id}), 200
        else:
            # Create a new wishlist
            wishlist_id = uuid.uuid4()
            cur.execute(
                "INSERT INTO wishlists (wishlist_id, user_id) VALUES (%s, %s)",
                (wishlist_id, str(user_id))
            )
            conn.commit()
            return jsonify({"message": "Wishlist created successfully", "wishlist_id": wishlist_id}), 201
    except Exception as e:
        app.logger.error(f"Error creating/getting wishlist for user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/wishlist/<uuid:user_id>/items", methods=["POST"])
def add_item_to_wishlist(user_id):
    """Adds a product to the user's wishlist."""
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"message": "Product ID is required"}), 400
    if not validate_user(str(user_id)):
        return jsonify({"message": "Invalid user ID"}), 400

    product_details = get_product_details(product_id)
    if not product_details:
        return jsonify({"message": "Product not found"}), 404

    conn = None
    r = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get wishlist_id for the user
        cur.execute("SELECT wishlist_id FROM wishlists WHERE user_id = %s", (str(user_id),))
        wishlist = cur.fetchone()
        if not wishlist:
            return jsonify({"message": "Wishlist not found for this user"}), 404
        wishlist_id = wishlist[0]

        # Check if item already exists in wishlist
        cur.execute(
            "SELECT item_id, quantity FROM wishlist_items WHERE wishlist_id = %s AND product_id = %s",
            (wishlist_id, product_id)
        )
        existing_item = cur.fetchone()

        if existing_item:
            # Update quantity if item exists
            new_quantity = existing_item[1] + quantity
            cur.execute(
                "UPDATE wishlist_items SET quantity = %s, added_date = CURRENT_TIMESTAMP WHERE item_id = %s",
                (new_quantity, existing_item[0])
            )
            message = "Product quantity updated in wishlist"
        else:
            # Add new item
            item_id = uuid.uuid4()
            cur.execute(
                "INSERT INTO wishlist_items (item_id, wishlist_id, product_id, quantity) VALUES (%s, %s, %s, %s)",
                (item_id, wishlist_id, product_id, quantity)
            )
            message = "Product added to wishlist"

        conn.commit()

        # Invalidate cache for this wishlist
        r = get_redis_connection()
        r.delete(f"wishlist:{user_id}")

        return jsonify({"message": message, "product_id": product_id}), 200
    except Exception as e:
        app.logger.error(f"Error adding item to wishlist for user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/wishlist/<uuid:user_id>/items", methods=["GET"])
def view_wishlist(user_id):
    """Retrieves all items in a user's wishlist."""
    if not validate_user(str(user_id)):
        return jsonify({"message": "Invalid user ID"}), 400

    r = None
    conn = None
    try:
        r = get_redis_connection()
        cached_wishlist = r.get(f"wishlist:{user_id}")
        if cached_wishlist:
            return jsonify(json.loads(cached_wishlist)), 200

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT wishlist_id FROM wishlists WHERE user_id = %s", (str(user_id),))
        wishlist_data = cur.fetchone()
        if not wishlist_data:
            return jsonify({"message": "Wishlist not found for this user", "items": []}), 200
        wishlist_id = wishlist_data[0]

        cur.execute(
            "SELECT product_id, quantity, status, added_date FROM wishlist_items WHERE wishlist_id = %s ORDER BY added_date DESC",
            (wishlist_id,)
        )
        items = cur.fetchall()

        wishlist_items = []
        for item in items:
            product_id, quantity, status, added_date = item
            product_details = get_product_details(product_id)
            wishlist_items.append({
                "product_id": product_id,
                "name": product_details["name"] if product_details else "Unknown Product",
                "price": product_details["price"] if product_details else None,
                "in_stock": product_details["in_stock"] if product_details else False,
                "quantity": quantity,
                "status": status,
                "added_date": added_date.isoformat()
            })
        
        response_data = {"user_id": user_id, "wishlist_id": wishlist_id, "items": wishlist_items}
        r.setex(f"wishlist:{user_id}", 300, json.dumps(response_data)) # Cache for 5 minutes

        return jsonify(response_data), 200
    except Exception as e:
        app.logger.error(f"Error viewing wishlist for user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/wishlist/<uuid:user_id>/items/<string:product_id>", methods=["DELETE"])
def remove_item_from_wishlist(user_id, product_id):
    """Removes a product from the user's wishlist."""
    if not validate_user(str(user_id)):
        return jsonify({"message": "Invalid user ID"}), 400

    conn = None
    r = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT wishlist_id FROM wishlists WHERE user_id = %s", (str(user_id),))
        wishlist = cur.fetchone()
        if not wishlist:
            return jsonify({"message": "Wishlist not found for this user"}), 404
        wishlist_id = wishlist[0]

        cur.execute(
            "DELETE FROM wishlist_items WHERE wishlist_id = %s AND product_id = %s RETURNING item_id",
            (wishlist_id, product_id)
        )
        deleted_item = cur.fetchone()
        conn.commit()

        if not deleted_item:
            return jsonify({"message": "Product not found in wishlist"}), 404
        
        # Invalidate cache
        r = get_redis_connection()
        r.delete(f"wishlist:{user_id}")

        return jsonify({"message": "Product removed from wishlist", "product_id": product_id}), 200
    except Exception as e:
        app.logger.error(f"Error removing item {product_id} from wishlist for user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/wishlist/<uuid:user_id>/items/<string:product_id>/move-to-cart", methods=["POST"])
def move_item_to_cart(user_id, product_id):
    """Moves a product from the wishlist to the shopping cart."""
    data = request.get_json()
    quantity = data.get("quantity", 1)

    if not validate_user(str(user_id)):
        return jsonify({"message": "Invalid user ID"}), 400

    product_details = get_product_details(product_id)
    if not product_details:
        return jsonify({"message": "Product not found"}), 404
    if not product_details.get("in_stock", False):
        # Update status in wishlist but keep it there
        conn = None
        r = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT wishlist_id FROM wishlists WHERE user_id = %s", (str(user_id),))
            wishlist = cur.fetchone()
            if wishlist:
                wishlist_id = wishlist[0]
                cur.execute(
                    "UPDATE wishlist_items SET status = %s WHERE wishlist_id = %s AND product_id = %s",
                    ("out_of_stock", wishlist_id, product_id)
                )
                conn.commit()
                r = get_redis_connection()
                r.delete(f"wishlist:{user_id}")
            return jsonify({"message": "Product is out of stock, cannot move to cart", "product_id": product_id, "status": "out_of_stock"}), 409
        except Exception as e:
            app.logger.error(f"Error updating status for out-of-stock product {product_id}: {e}")
            return jsonify({"message": "Internal server error during status update"}), 500
        finally:
            if conn:
                conn.close()

    # Simulate adding to cart
    if not add_to_shopping_cart(str(user_id), product_id, quantity):
        return jsonify({"message": "Failed to add product to shopping cart"}), 500

    conn = None
    r = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT wishlist_id FROM wishlists WHERE user_id = %s", (str(user_id),))
        wishlist = cur.fetchone()
        if not wishlist:
            return jsonify({"message": "Wishlist not found for this user"}), 404
        wishlist_id = wishlist[0]

        # Remove from wishlist after moving to cart
        cur.execute(
            "DELETE FROM wishlist_items WHERE wishlist_id = %s AND product_id = %s RETURNING item_id",
            (wishlist_id, product_id)
        )
        deleted_item = cur.fetchone()
        conn.commit()

        if not deleted_item:
            return jsonify({"message": "Product not found in wishlist to move"}), 404

        # Invalidate cache
        r = get_redis_connection()
        r.delete(f"wishlist:{user_id}")

        return jsonify({"message": "Product moved to cart successfully", "product_id": product_id}), 200
    except Exception as e:
        app.logger.error(f"Error moving item {product_id} to cart for user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/wishlist/<uuid:user_id>/share", methods=["POST"])
def share_wishlist(user_id):
    """Generates a shareable link for the wishlist and optionally sends it via email."""
    data = request.get_json()
    recipient_emails = data.get("recipient_emails", [])

    if not validate_user(str(user_id)):
        return jsonify({"message": "Invalid user ID"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT wishlist_id FROM wishlists WHERE user_id = %s", (str(user_id),))
        wishlist = cur.fetchone()
        if not wishlist:
            return jsonify({"message": "Wishlist not found for this user"}), 404
        wishlist_id = wishlist[0]

        # Generate a unique shareable link (simplified for this example)
        share_token = str(uuid.uuid4())
        share_link = f"https://your-ecommerce.com/wishlist/share/{share_token}"
        
        # In a real app, you'd store this token and associated wishlist_id in a database
        # For now, just simulate sending notification
        if recipient_emails:
            send_share_notification(str(user_id), share_link, recipient_emails)

        return jsonify({"message": "Wishlist share link generated", "share_link": share_link}), 200
    except Exception as e:
        app.logger.error(f"Error sharing wishlist for user {user_id}: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)

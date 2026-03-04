# Wishlist Service

This is a Flask-based microservice for managing user wishlists, as specified in Jira issue [SCRUM-10](https://bfsi-na-ai-engineering.atlassian.net/browse/SCRUM-10) and its associated High-Level Design (HLD) document.

## Features

- Add products to a personal wishlist.
- View all items in a personal wishlist.
- Remove products from a wishlist.
- Move products from a wishlist directly to the shopping cart.
- Share a wishlist via a unique link or email.
- Persistence of wishlist items for registered users across sessions and devices.
- Handles empty wishlist states.

## Architecture

This service is part of a larger e-commerce microservices ecosystem. It interacts with:

- **PostgreSQL Database**: For persistent storage of wishlist and wishlist item data.
- **Redis Cache**: For caching frequently accessed wishlist data to improve performance.
- **Product Catalog Service (simulated)**: To fetch product details.
- **User Service (simulated)**: For user validation.
- **Shopping Cart Service (simulated)**: To move items to the user's cart.
- **Notification Service (simulated)**: To send share notifications.

## Technologies Used

- Python 3.9+
- Flask (Web Framework)
- PostgreSQL (Database)
- Redis (Cache)
- Docker (Containerization)
- Google Cloud Platform (GCP) - (Conceptual deployment target: GKE, Cloud SQL, Memorystore for Redis)

## Setup and Local Development

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized setup)
- PostgreSQL database instance
- Redis instance

### 1. Clone the repository

```bash
git clone https://github.com/p67428378-afk/web-todo-app.git
cd web-todo-app
```

### 2. Set up Environment Variables

Create a `.env` file in the root directory of the project based on `.env.example`:

```ini
# .env
DATABASE_URL="postgresql://user:password@localhost:5432/wishlist_db"
REDIS_URL="redis://localhost:6379/0"
```

Replace `user`, `password`, `localhost:5432`, `wishlist_db`, and `localhost:6379` with your actual database and Redis connection details.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
flask run
```

The application will run on `http://127.0.0.1:5000` by default.

### 5. Run with Docker (Optional)

Ensure Docker is installed and running.

```bash
docker build -t wishlist-service .
docker run -p 5000:5000 --env-file ./.env wishlist-service
```

## API Endpoints

Base URL: `http://127.0.0.1:5000`

### 1. Health Check

- `GET /`
- **Description**: Checks if the service is running.
- **Response**: `{"status": "Wishlist Service is up and running!"}`

### 2. Create or Get Wishlist

- `POST /wishlist/<user_id>`
- **Description**: Creates a new wishlist for a user if one doesn't exist, or returns the existing one.
- **Parameters**:
    - `user_id` (path): UUID of the user.
- **Example Request**:
    ```bash
    curl -X POST http://127.0.0.1:5000/wishlist/a1b2c3d4-e5f6-7890-1234-567890abcdef
    ```
- **Example Response (New)**:
    ```json
    {
        "message": "Wishlist created successfully",
        "wishlist_id": "<uuid>"
    }
    ```
- **Example Response (Existing)**:
    ```json
    {
        "message": "Wishlist already exists",
        "wishlist_id": "<uuid>"
    }
    ```

### 3. Add Item to Wishlist

- `POST /wishlist/<user_id>/items`
- **Description**: Adds a product to the user's wishlist. If the product already exists, its quantity is updated.
- **Parameters**:
    - `user_id` (path): UUID of the user.
- **Request Body**:
    ```json
    {
        "product_id": "prod123",
        "quantity": 1
    }
    ```
- **Example Request**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"product_id": "prod123", "quantity": 1}' http://127.0.0.1:5000/wishlist/a1b2c3d4-e5f6-7890-1234-567890abcdef/items
    ```
- **Example Response**:
    ```json
    {
        "message": "Product added to wishlist",
        "product_id": "prod123"
    }
    ```

### 4. View Wishlist

- `GET /wishlist/<user_id>/items`
- **Description**: Retrieves all items in a user's wishlist.
- **Parameters**:
    - `user_id` (path): UUID of the user.
- **Example Request**:
    ```bash
    curl http://127.0.0.1:5000/wishlist/a1b2c3d4-e5f6-7890-1234-567890abcdef/items
    ```
- **Example Response**:
    ```json
    {
        "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "wishlist_id": "<uuid>",
        "items": [
            {
                "product_id": "prod123",
                "name": "Laptop Pro",
                "price": 1200.0,
                "in_stock": true,
                "quantity": 1,
                "status": "active",
                "added_date": "2026-03-04T10:00:00"
            }
        ]
    }
    ```

### 5. Remove Item from Wishlist

- `DELETE /wishlist/<user_id>/items/<product_id>`
- **Description**: Removes a specific product from the user's wishlist.
- **Parameters**:
    - `user_id` (path): UUID of the user.
    - `product_id` (path): ID of the product to remove.
- **Example Request**:
    ```bash
    curl -X DELETE http://127.0.0.1:5000/wishlist/a1b2c3d4-e5f6-7890-1234-567890abcdef/items/prod123
    ```
- **Example Response**:
    ```json
    {
        "message": "Product removed from wishlist",
        "product_id": "prod123"
    }
    ```

### 6. Move Item to Cart

- `POST /wishlist/<user_id>/items/<product_id>/move-to-cart`
- **Description**: Moves a product from the wishlist to the shopping cart. If the product is out of stock, it remains in the wishlist with an updated status.
- **Parameters**:
    - `user_id` (path): UUID of the user.
    - `product_id` (path): ID of the product to move.
- **Request Body**:
    ```json
    {
        "quantity": 1
    }
    ```
- **Example Request**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"quantity": 1}' http://127.0.0.1:5000/wishlist/a1b2c3d4-e5f6-7890-1234-567890abcdef/items/prod123/move-to-cart
    ```
- **Example Response (Success)**:
    ```json
    {
        "message": "Product moved to cart successfully",
        "product_id": "prod123"
    }
    ```
- **Example Response (Out of Stock)**:
    ```json
    {
        "message": "Product is out of stock, cannot move to cart",
        "product_id": "prod789",
        "status": "out_of_stock"
    }
    ```

### 7. Share Wishlist

- `POST /wishlist/<user_id>/share`
- **Description**: Generates a shareable link for the wishlist and optionally sends it to specified email addresses.
- **Parameters**:
    - `user_id` (path): UUID of the user.
- **Request Body (Optional)**:
    ```json
    {
        "recipient_emails": ["friend1@example.com", "friend2@example.com"]
    }
    ```
- **Example Request**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"recipient_emails": ["test@example.com"]}' http://127.0.0.1:5000/wishlist/a1b2c3d4-e5f6-7890-1234-567890abcdef/share
    ```
- **Example Response**:
    ```json
    {
        "message": "Wishlist share link generated",
        "share_link": "https://your-ecommerce.com/wishlist/share/<uuid>"
    }
    ```

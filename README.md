# Social Media Comment Dislike Feature (SCRUM-13)

This project implements a backend API for adding a "dislike" button functionality to comments on a social media platform, as specified in Jira issue SCRUM-13.

## Features

-   **Dislike/Undislike Comments**: Users can dislike a comment, and remove their dislike.
-   **Like/Unlike Comments**: Users can like a comment, and remove their like.
-   **Mutual Exclusivity**: A user cannot like and dislike the same comment simultaneously. Performing one action will remove the other.
-   **Dislike Count**: Retrieve the current dislike count for any comment.
-   **Database Integration**: Stores user reactions (likes/dislikes) in a database.

## Technology Stack

-   **Backend**: Python with Flask
-   **Database**: SQLAlchemy ORM with SQLite (for development/example), easily adaptable to PostgreSQL for production.

## Setup Instructions

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/p67428378-afk/web-todo-app.git
    cd web-todo-app
    git checkout ISSUE-SCRUM-13
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application**:

    ```bash
    python app.py
    ```

    The API will be running on `http://127.0.0.1:5000`.

## API Endpoints

### Dislike a Comment

-   **URL**: `/comments/<int:comment_id>/dislike`
-   **Method**: `POST`
-   **Body**: `{"user_id": <int>}` (In a real app, `user_id` would come from authentication)
-   **Example Request**:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1}' http://127.0.0.1:5000/comments/1/dislike
    ```

-   **Responses**:
    -   `201 Created`: `{"message": "Comment disliked", "status": "disliked"}`
    -   `200 OK`: `{"message": "Dislike removed", "status": "undisliked"}` (if already disliked)
    -   `200 OK`: `{"message": "Changed from like to dislike", "status": "disliked"}` (if previously liked)

### Get Dislike Count for a Comment

-   **URL**: `/comments/<int:comment_id>/dislikes`
-   **Method**: `GET`
-   **Example Request**:

    ```bash
    curl http://127.0.0.1:5000/comments/1/dislikes
    ```

-   **Response**:
    -   `200 OK`: `{"comment_id": 1, "dislike_count": 5}`

### Like a Comment

-   **URL**: `/comments/<int:comment_id>/like`
-   **Method**: `POST`
-   **Body**: `{"user_id": <int>}`
-   **Example Request**:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1}' http://127.0.0.1:5000/comments/1/like
    ```

-   **Responses**:
    -   `201 Created`: `{"message": "Comment liked", "status": "liked"}`
    -   `200 OK`: `{"message": "Like removed", "status": "unliked"}` (if already liked)
    -   `200 OK`: `{"message": "Changed from dislike to like", "status": "liked"}` (if previously disliked)

## Database Schema

The `database.py` file defines the following SQLAlchemy models:

-   `User`: Represents a user.
-   `Comment`: Represents a comment.
-   `Reaction`: Stores user reactions (like/dislike) to comments. Includes `user_id`, `comment_id`, and `reaction_type`.

## Real-time Updates

For real-time updates of dislike counts (as per acceptance criteria), a WebSocket implementation (e.g., using Flask-SocketIO) would be required. This API provides the core logic and endpoints, and can be integrated with a WebSocket layer to push updates to connected clients.

## Security Considerations

-   **Authentication**: The current `user_id` is a placeholder. In a production environment, this should be replaced with a robust authentication system (e.g., JWT, OAuth) to identify the authenticated user.
-   **Rate Limiting**: Implement rate limiting on the dislike/like endpoints to prevent abuse and automated actions.
-   **Input Validation**: Ensure all incoming data is properly validated to prevent injection attacks and other vulnerabilities.

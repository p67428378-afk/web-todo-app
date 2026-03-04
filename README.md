# Web Todo App - Comment Liking Feature (SCRUM-12)

This branch introduces the functionality for users to like and unlike comments within the application, along with displaying the like count.

## Database Changes

The following changes have been applied to the database schema:

-   An `likes_count` column has been added to the `comments` table to store the total number of likes for each comment.
-   A new `comment_likes` table has been created to track which user liked which comment.

To apply these changes to your local database, run the SQL script:

```sql
-- File: database_schema.sql

-- Add a likes_count column to the existing comments table
ALTER TABLE comments
ADD COLUMN likes_count INTEGER DEFAULT 0;

-- Create a new table to store comment likes
CREATE TABLE comment_likes (
    user_id INTEGER NOT NULL,
    comment_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, comment_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE
);
```

**Note**: The `ON DELETE CASCADE` clauses ensure that:
-   If a user account is deleted, all their associated likes are automatically removed.
-   If a comment is deleted, all its associated likes are automatically removed.
This addresses the "Edge Case: User Account Deletion" and "Edge Case: Comment Deletion" acceptance criteria.

## API Endpoints

The following API endpoints have been added/modified to support the comment liking feature:

### 1. Like a Comment

-   **Endpoint**: `POST /comments/<int:comment_id>/like`
-   **Description**: Allows the authenticated user to like a specific comment. A user can only like a comment once.
-   **Authentication**: Required (assumes `current_user` is available).
-   **Responses**:
    -   `200 OK`: `{"message": "Comment liked successfully"}`
    -   `401 Unauthorized`: If the user is not authenticated.
    -   `404 Not Found`: If the `comment_id` does not exist.
    -   `409 Conflict`: `{"message": "Comment already liked by this user"}`

### 2. Unlike a Comment

-   **Endpoint**: `DELETE /comments/<int:comment_id>/like`
-   **Description**: Allows the authenticated user to remove their like from a specific comment.
-   **Authentication**: Required.
-   **Responses**:
    -   `200 OK`: `{"message": "Comment unliked successfully"}`
    -   `401 Unauthorized`: If the user is not authenticated.
    -   `404 Not Found`: If the `comment_id` does not exist or the user has not liked the comment.

### 3. Get Comment Details with Like Status

-   **Endpoint**: `GET /comments/<int:comment_id>`
-   **Description**: Retrieves details for a specific comment, including its total `likes_count` and a boolean `user_liked` indicating if the current authenticated user has liked it.
-   **Authentication**: Optional (if authenticated, `user_liked` will be accurate; otherwise, it might default to `false` or be omitted).
-   **Responses**:
    -   `200 OK`:
        ```json
        {
            "comment_id": 123,
            "content": "This is a sample comment content.",
            "likes_count": 5,
            "user_liked": true
        }
        ```
    -   `404 Not Found`: If the `comment_id` does not exist.

## Backend Implementation Notes

-   The core logic is implemented in `app/routes/comment_likes.py`.
-   It uses a `MockDB` and `MockUser` for demonstration purposes. In a production environment, these should be replaced with your actual database ORM (e.g., SQLAlchemy) and user authentication system.
-   The `likes_count` in the `comments` table is automatically incremented/decremented upon liking/unliking.

## Future Considerations

-   **Comment Sorting**: The `likes_count` column can be used to implement sorting comments by popularity. This would involve modifying the comment retrieval queries.
-   **Frontend Integration**: The frontend would need to be updated to:
    -   Display the like count.
    -   Render a "Like" button that visually changes based on `user_liked` status.
    -   Call the `POST` and `DELETE` like endpoints.

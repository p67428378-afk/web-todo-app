# File: app/routes/comment_likes.py

"""
Module: comment_likes
Purpose: Handles liking and unliking comments, and managing like counts.
Author: Developer_Agent
Created: 2023-10-27
Notes: This module assumes a Flask-like application structure with a 'db' object for database
       interaction and a 'current_user' object for authenticated user information.
"""

from flask import Blueprint, jsonify, request, abort
# Assuming 'db' and 'Comment' model are imported from your application's models
# from app.models import db, Comment, CommentLike, User # Example imports

# Placeholder for database and models - replace with actual imports/setup
class MockDB:
    def execute(self, query, params=None):
        print(f"Executing query: {query} with params: {params}")
        # Simulate DB operations
        if "INSERT" in query:
            return {"rowcount": 1}
        elif "DELETE" in query:
            return {"rowcount": 1}
        elif "SELECT" in query and "comment_likes" in query:
            # Simulate a like existing or not
            if params and params.get('user_id') == 1 and params.get('comment_id') == 1:
                return [{"user_id": 1, "comment_id": 1}]
            return []
        return []

    def commit(self):
        print("Committing transaction")

db = MockDB()

class MockComment:
    def __init__(self, id, likes_count=0):
        self.id = id
        self.likes_count = likes_count

    @classmethod
    def get(cls, comment_id):
        # Simulate fetching a comment
        if comment_id == 1:
            return MockComment(id=1, likes_count=5) # Example comment with 5 likes
        return None

    def save(self):
        print(f"Saving comment {self.id} with likes_count {self.likes_count}")

class MockUser:
    def __init__(self, id):
        self.id = id

current_user = MockUser(id=1) # Simulate an authenticated user with ID 1


comment_likes_bp = Blueprint('comment_likes', __name__)

@comment_likes_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id: int):
    """
    Allows a user to like a specific comment.

    Args:
        comment_id (int): The ID of the comment to like.

    Returns:
        jsonify: A JSON response indicating success or failure.
    """
    user_id = current_user.id

    # Check if the user has already liked this comment
    query = "SELECT * FROM comment_likes WHERE user_id = :user_id AND comment_id = :comment_id"
    existing_like = db.execute(query, {'user_id': user_id, 'comment_id': comment_id})

    if existing_like:
        return jsonify({"message": "Comment already liked by this user"}), 409 # Conflict

    # Add the like
    insert_query = "INSERT INTO comment_likes (user_id, comment_id) VALUES (:user_id, :comment_id)"
    db.execute(insert_query, {'user_id': user_id, 'comment_id': comment_id})

    # Increment the likes_count in the comments table
    update_comment_query = "UPDATE comments SET likes_count = likes_count + 1 WHERE comment_id = :comment_id"
    db.execute(update_comment_query, {'comment_id': comment_id})

    db.commit()
    return jsonify({"message": "Comment liked successfully"}), 200

@comment_likes_bp.route('/comments/<int:comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id: int):
    """
    Allows a user to unlike a specific comment.

    Args:
        comment_id (int): The ID of the comment to unlike.

    Returns:
        jsonify: A JSON response indicating success or failure.
    """
    user_id = current_user.id

    # Check if the user has liked this comment
    query = "SELECT * FROM comment_likes WHERE user_id = :user_id AND comment_id = :comment_id"
    existing_like = db.execute(query, {'user_id': user_id, 'comment_id': comment_id})

    if not existing_like:
        return jsonify({"message": "Comment not liked by this user"}), 404 # Not Found

    # Remove the like
    delete_query = "DELETE FROM comment_likes WHERE user_id = :user_id AND comment_id = :comment_id"
    db.execute(delete_query, {'user_id': user_id, 'comment_id': comment_id})

    # Decrement the likes_count in the comments table
    update_comment_query = "UPDATE comments SET likes_count = likes_count - 1 WHERE comment_id = :comment_id"
    db.execute(update_comment_query, {'comment_id': comment_id})

    db.commit()
    return jsonify({"message": "Comment unliked successfully"}), 200

# This would typically be part of the comment retrieval endpoint, not a separate one.
# For demonstration, I'll show how to get like status and count.
@comment_likes_bp.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment_with_like_status(comment_id: int):
    """
    Retrieves a comment along with its like count and the current user's like status.

    Args:
        comment_id (int): The ID of the comment to retrieve.

    Returns:
        jsonify: A JSON response containing comment details, like count, and like status.
    """
    # In a real application, you'd fetch the comment from the database
    # For this example, we'll use a mock comment
    comment = MockComment.get(comment_id)
    if not comment:
        abort(404, description="Comment not found")

    user_id = current_user.id
    query = "SELECT * FROM comment_likes WHERE user_id = :user_id AND comment_id = :comment_id"
    user_liked = bool(db.execute(query, {'user_id': user_id, 'comment_id': comment_id}))

    return jsonify({
        "comment_id": comment.id,
        "content": "This is a sample comment content.", # Placeholder
        "likes_count": comment.likes_count,
        "user_liked": user_liked
    }), 200

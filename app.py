"""
Module: app
Purpose: Flask application for handling comment likes/unlikes.
Author: Developer_Agent
Created: 2023-10-27
Notes: Implements API endpoints for liking and unliking comments, and serves the frontend.
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory store for comments and their likes.
# In a real application, this would be a database.
# Define the initial state of comments_db
_initial_comments_db_state = {
    "1": {"text": "Great post!", "likes": 0, "liked_by": []},
    "2": {"text": "Very insightful.", "likes": 0, "liked_by": []},
    "3": {"text": "I disagree with this point.", "likes": 0, "liked_by": []},
}

# Global variable for comments_db
comments_db = {}

def initialize_comments_db():
    """
    Initializes or resets the comments_db to its default state.
    """
    global comments_db
    comments_db = {k: v.copy() for k, v in _initial_comments_db_state.items()}

# Initialize comments_db when the application starts
initialize_comments_db()

@app.route('/')
def index():
    """
    Renders the main page with comments.
    """
    return render_template('index.html', comments=comments_db)

@app.route('/api/like/<comment_id>', methods=['POST'])
def like_comment(comment_id: str):
    """
    Handles liking a comment.

    Args:
        comment_id (str): The ID of the comment to like.

    Returns:
        json: Updated comment data or an error message.
    """
    global comments_db # Explicitly declare comments_db as global
    user_id = request.json.get('user_id', 'anonymous') # In a real app, user_id would come from authentication

    if comment_id not in comments_db:
        return jsonify({"error": "Comment not found"}), 404

    comment = comments_db[comment_id]
    if user_id in comment['liked_by']:
        return jsonify({"message": "User already liked this comment", "comment": comment}), 200
    
    comment['likes'] += 1
    comment['liked_by'].append(user_id)
    return jsonify({"message": "Comment liked successfully", "comment": comment}), 200

@app.route('/api/unlike/<comment_id>', methods=['POST'])
def unlike_comment(comment_id: str):
    """
    Handles unliking a comment.

    Args:
        comment_id (str): The ID of the comment to unlike.

    Returns:
        json: Updated comment data or an error message.
    """
    global comments_db # Explicitly declare comments_db as global
    user_id = request.json.get('user_id', 'anonymous') # In a real app, user_id would come from authentication

    if comment_id not in comments_db:
        return jsonify({"error": "Comment not found"}), 404

    comment = comments_db[comment_id]
    if user_id not in comment['liked_by']:
        return jsonify({"message": "User has not liked this comment", "comment": comment}), 200
    
    comment['likes'] -= 1
    comment['liked_by'].remove(user_id)
    return jsonify({"message": "Comment unliked successfully", "comment": comment}), 200

@app.route('/api/comments', methods=['GET'])
def get_comments():
    """
    Returns all comments, optionally sorted by popularity.
    """
    sort_by = request.args.get('sort_by')
    
    comments_list = []
    for comment_id, comment_data in comments_db.items():
        comment_data_copy = comment_data.copy()
        comment_data_copy['id'] = comment_id
        comments_list.append(comment_data_copy)

    if sort_by == 'popularity':
        # Sort the list of comment dictionaries by 'likes' in descending order
        sorted_comments = sorted(comments_list, key=lambda comment: comment['likes'], reverse=True)
        return jsonify(sorted_comments), 200
    
    return jsonify(comments_list), 200

# Edge case: Simulate user account deletion
@app.route('/api/delete_user_likes/<user_id>', methods=['POST'])
def delete_user_likes(user_id: str):
    """
    Simulates user account deletion by removing all likes from a specific user.

    Args:
        user_id (str): The ID of the user whose likes should be removed.

    Returns:
        json: A message indicating the outcome.
    """
    global comments_db # Explicitly declare comments_db as global
    likes_removed_count = 0
    for comment_id, comment in comments_db.items():
        # Create a mutable copy of liked_by for safe modification during iteration
        if user_id in comment['liked_by']:
            comment['liked_by'].remove(user_id)
            comment['likes'] -= 1
            likes_removed_count += 1
    return jsonify({"message": f"Removed {likes_removed_count} likes for user {user_id}"}), 200

# Edge case: Simulate comment deletion
@app.route('/api/delete_comment/<comment_id>', methods=['POST'])
def delete_comment_endpoint(comment_id: str):
    """
    Simulates comment deletion by removing the comment and its associated likes.

    Args:
        comment_id (str): The ID of the comment to delete.

    Returns:
        json: A message indicating the outcome.
    """
    global comments_db # Explicitly declare comments_db as global
    if comment_id in comments_db:
        del comments_db[comment_id]
        return jsonify({"message": f"Comment {comment_id} and its likes deleted."}), 200
    return jsonify({"error": "Comment not found"}), 404

@app.route('/api/reset_comments', methods=['POST'])
def reset_comments():
    """
    Resets the comments_db to its initial state.
    This endpoint is primarily for testing purposes.
    """
    initialize_comments_db()
    return jsonify({"message": "Comments database reset to initial state."}), 200


if __name__ == '__main__':
    app.run(debug=True)

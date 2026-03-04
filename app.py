from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal, User, Comment, Reaction, engine, Base

app = Flask(__name__)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to get a new DB session (for routes)
def get_db_session():
    return next(get_db())

@app.route("/comments/<int:comment_id>/dislike", methods=["POST"])
def dislike_comment(comment_id):
    # In a real application, you would get the user_id from the authenticated user session
    # For this example, we'll assume a user_id is sent in the request body or is a placeholder.
    # For simplicity, let's assume user_id = 1 for now.
    user_id = request.json.get("user_id", 1) # Placeholder for authenticated user

    db: Session = get_db_session()

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Create a dummy user if not exists for testing purposes
        user = User(id=user_id, username=f"user_{user_id}")
        db.add(user)
        db.commit()
        db.refresh(user)

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        # Create a dummy comment if not exists for testing purposes
        comment = Comment(id=comment_id, text=f"This is comment {comment_id}", user_id=user_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)

    existing_reaction = db.query(Reaction).filter(
        Reaction.user_id == user_id,
        Reaction.comment_id == comment_id
    ).first()

    if existing_reaction:
        if existing_reaction.reaction_type == "dislike":
            # User already disliked, so remove the dislike
            db.delete(existing_reaction)
            db.commit()
            return jsonify({"message": "Dislike removed", "status": "undisliked"}), 200
        else:
            # User liked, change to dislike (remove like, add dislike)
            existing_reaction.reaction_type = "dislike"
            db.commit()
            db.refresh(existing_reaction)
            return jsonify({"message": "Changed from like to dislike", "status": "disliked"}), 200
    else:
        # No existing reaction, add dislike
        new_dislike = Reaction(user_id=user_id, comment_id=comment_id, reaction_type="dislike")
        db.add(new_dislike)
        db.commit()
        db.refresh(new_dislike)
        return jsonify({"message": "Comment disliked", "status": "disliked"}), 201

@app.route("/comments/<int:comment_id>/dislikes", methods=["GET"])
def get_dislike_count(comment_id):
    db: Session = get_db_session()
    dislike_count = db.query(Reaction).filter(
        Reaction.comment_id == comment_id,
        Reaction.reaction_type == "dislike"
    ).count()
    return jsonify({"comment_id": comment_id, "dislike_count": dislike_count}), 200

@app.route("/comments/<int:comment_id>/like", methods=["POST"])
def like_comment(comment_id):
    user_id = request.json.get("user_id", 1) # Placeholder for authenticated user

    db: Session = get_db_session()

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, username=f"user_{user_id}")
        db.add(user)
        db.commit()
        db.refresh(user)

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        comment = Comment(id=comment_id, text=f"This is comment {comment_id}", user_id=user_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)

    existing_reaction = db.query(Reaction).filter(
        Reaction.user_id == user_id,
        Reaction.comment_id == comment_id
    ).first()

    if existing_reaction:
        if existing_reaction.reaction_type == "like":
            # User already liked, so remove the like
            db.delete(existing_reaction)
            db.commit()
            return jsonify({"message": "Like removed", "status": "unliked"}), 200
        else:
            # User disliked, change to like (remove dislike, add like)
            existing_reaction.reaction_type = "like"
            db.commit()
            db.refresh(existing_reaction)
            return jsonify({"message": "Changed from dislike to like", "status": "liked"}), 200
    else:
        # No existing reaction, add like
        new_like = Reaction(user_id=user_id, comment_id=comment_id, reaction_type="like")
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return jsonify({"message": "Comment liked", "status": "liked"}), 201


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine) # Ensure tables are created
    app.run(debug=True)

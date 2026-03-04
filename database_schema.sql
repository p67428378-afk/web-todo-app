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
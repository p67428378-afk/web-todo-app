# Web Todo App with Comment Liking Feature

This project implements a simple web application using Flask for the backend and basic HTML/CSS/JavaScript for the frontend. It demonstrates how users can like and unlike comments, view like counts, and sort comments by popularity. It also includes API endpoints to simulate user and comment deletion for edge case testing.

## Features

-   **Like/Unlike Comments**: Users can like and unlike comments. A user can only like a comment once.
-   **Display Like Count**: The current number of likes for each comment is displayed.
-   **Sort by Popularity**: Comments can be sorted based on their like count.
-   **User Account Deletion (Simulated)**: API endpoint to simulate a user deleting their account, which removes all their associated likes.
-   **Comment Deletion (Simulated)**: API endpoint to simulate a comment being deleted, which removes the comment and all its likes.

## Project Structure

```
.gitignore
app.py
requirements.txt
README.md
static/
â””â”€â”€ css/
    â””â”€â”€ style.css
â””â”€â”€ js/
    â””â”€â”€ script.js
templates/
â””â”€â”€ index.html
```

-   `app.py`: The main Flask application, defining routes for the web pages and API endpoints.
-   `requirements.txt`: Lists the Python dependencies.
-   `static/css/style.css`: Contains the styling for the web application.
-   `static/js/script.js`: Handles frontend interactivity, including like/unlike actions and sorting.
-   `templates/index.html`: The main HTML template that displays the comments.

## Setup and Run Instructions

Follow these steps to set up and run the application locally:

### 1. Clone the Repository

```bash
git clone https://github.com/p67428378-afk/web-todo-app.git
cd web-todo-app
```

### 2. Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application

Set the Flask application and run it:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development # For development mode with debug features
flask run
```

Alternatively, you can run it directly:

```bash
python app.py
```

The application will typically run on `http://127.0.0.1:5000/`. Open this URL in your web browser.

## Usage

-   **Liking/Unliking**: Click the "Like" button next to any comment to toggle its like status. The like count will update accordingly.
-   **Sorting**: Use the "Default" and "Popularity" buttons to sort the comments.

## API Endpoints

The following API endpoints are available (used by the frontend):

-   `GET /api/comments`: Get all comments. Supports `?sort_by=popularity`.
-   `POST /api/like/<comment_id>`: Like a comment. Requires `user_id` in JSON body.
-   `POST /api/unlike/<comment_id>`: Unlike a comment. Requires `user_id` in JSON body.
-   `POST /api/delete_user_likes/<user_id>`: (Simulated) Remove all likes by a specific user.
-   `POST /api/delete_comment/<comment_id>`: (Simulated) Delete a comment and its likes.

## Testing Edge Cases (Manual)

You can manually test the simulated edge cases using tools like `curl` or Postman:

### Simulate User Account Deletion

To remove all likes from `user123` (as used in `script.js`):

```bash
curl -X POST http://127.0.0.1:5000/api/delete_user_likes/user123
```

Refresh the main page to see the updated like counts.

### Simulate Comment Deletion

To delete comment with ID `1`:

```bash
curl -X POST http://127.0.0.1:5000/api/delete_comment/1
```

Refresh the main page to see comment `1` removed.

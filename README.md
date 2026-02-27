# Web To Do App

This project implements a simple web-based to-do application with a dummy login page, built using React.js and styled with Tailwind CSS. It fulfills the requirements of Jira issue SCRUM-19.

## Features

- **Dummy Login Page**: A simulated login interface with fields for Email, Username, and Password. Upon clicking 'Login', it redirects to the To-Do list without actual authentication.
- **To-Do List Functionality**: Users can:
    - Add new tasks.
    - Mark existing tasks as 'done'.
    - Delete tasks.
- **Client-Side Data Storage**: To-Do items are stored in the browser's local storage, providing persistence across sessions for a single user.

## Technical Stack

- **Frontend**: React.js
- **Styling**: Tailwind CSS
- **State Management**: React's `useState` and `useEffect` hooks.
- **Local Storage**: Browser's `localStorage` API.
- **Unique IDs**: `uuid` library for generating unique task IDs.

## Project Structure

```
web-todo-app/
├── public/
│   └── index.html              # Main HTML file
├── src/
│   ├── App.js                  # Main application component, handles routing
│   ├── index.js                # React entry point
│   ├── components/
│   │   ├── LoginPage.js        # Dummy login page component
│   │   ├── TodoList.js         # To-Do list management component
│   │   └── TodoItem.js         # Individual To-Do item component
│   ├── css/
│   │   └── index.css           # Tailwind CSS imports and custom styles
│   └── utils/
│       └── localStorage.js     # Utility for local storage operations
├── .gitignore                  # Git ignore file
├── package.json                # Project dependencies and scripts
├── README.md                   # Project documentation
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
```

## Setup and Installation

To get this project up and running on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/web-todo-app.git
    cd web-todo-app
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```

3.  **Run the application:**
    ```bash
    npm start
    # or
    yarn start
    ```

    The application will open in your browser at `http://localhost:3000` (or another available port).

## Usage

1.  **Login Page**: You will first see a login page. Enter any values for Email, Username, and Password, then click the 'Login' button. This will simulate a successful login and redirect you to the To-Do list.
2.  **To-Do List**: 
    -   **Add Task**: Type a task description into the input field and click 'Add Task'.
    -   **Mark as Done/Undo**: Click the 'Done' button next to a task to mark it as complete. Click 'Undo' to revert its status.
    -   **Delete Task**: Click the 'Delete' button next to a task to remove it from the list.

Your tasks will be saved in your browser's local storage and will persist even if you close and reopen the browser tab.

## Contributing

This project was developed to fulfill a specific Jira task (SCRUM-19). For future enhancements or bug fixes, please refer to the project's contribution guidelines (if any) or create a new Jira issue.

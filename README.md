# Employee Leave Application Portal

This project implements an Employee Leave Application Portal as described in Jira story SCRUM-17. It consists of a FastAPI backend and a React (TypeScript) frontend.

## Architecture

- **Frontend**: React with TypeScript
- **Backend**: Python with FastAPI
- **Database**: PostgreSQL
- **Authentication**: OAuth2/JWT
- **Deployment**: Docker, Kubernetes (future)

## Features

- **Leave Type Selection**: Employees can select from Casual Leave, Sick Leave, Earned Leave, and Flexi Holiday.
- **Leave Request Submission**: Employees can specify dates and reasons for leave.
- **Approval Workflows**:
    - Flexi Holiday & Sick Leave: Automatic approval.
    - Casual & Earned Leave: Manager approval required.
- **Leave Status Tracking**: Employees can view the status of their requests.
- **Leave Balance Display**: Current leave balances are shown for each leave type.
- **Data Security**: Secure storage and transmission of sensitive data.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js and npm/yarn (for frontend development)

### Backend Setup

1.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Environment Variables**: Create a `.env` file in the `backend` directory based on `.env.example`.

4.  **Run the database (PostgreSQL) and backend using Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    The backend API will be available at `http://localhost:8000`.

### Frontend Setup (Placeholder)

1.  **Navigate to the `frontend` directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```

3.  **Run the frontend development server:**
    ```bash
    npm start
    # or yarn start
    ```
    The frontend application will be available at `http://localhost:3000`.

## API Endpoints

- `POST /auth/register`: Register a new user.
- `POST /auth/token`: Obtain JWT token for authentication.
- `POST /leave/apply`: Apply for leave.
- `GET /leave/status`: Get current user's leave requests.
- `GET /leave/balance`: Get current user's leave balances.
- `PUT /leave/{request_id}/approve`: Approve a leave request (Manager only).
- `PUT /leave/{request_id}/reject`: Reject a leave request (Manager only).

## Database Schema

- `users`: Stores user information (email, hashed_password, role).
- `leave_types`: Stores available leave types (Casual, Sick, Earned, Flexi Holiday).
- `leave_requests`: Stores details of each leave application.
- `leave_balances`: Stores current leave balances for each user and leave type.

## Contributing

Refer to the project's coding standards and guidelines.

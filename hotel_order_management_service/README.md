# Hotel Order Management Service

This service is designed to manage room service orders within a hotel environment, integrating with a Property Management System (PMS) and tracking inventory for room service items.

## Features

*   **Order Creation and Management:** Create, view, modify, and cancel room service orders. Track real-time order status.
*   **PMS Integration:** Seamlessly integrate with an existing PMS to retrieve guest information and update billing records.
*   **Inventory Tracking:** Real-time inventory tracking for room service items with alerts for low stock.
*   **Security:** Encrypted data transmission, role-based access control, and regular security audits.
*   **Reporting and Analytics:** Generate reports on order volume, popular items, and delivery times.

## Architecture

The service follows a microservices architecture, deployed on Google Cloud Platform (GCP) using Docker and Kubernetes.

### Core Services

*   **Order Management Service:** Handles the lifecycle of room service orders.
*   **PMS Integration Service:** Manages communication with the Property Management System.
*   **Inventory Management Service:** Tracks and manages the stock levels of room service items.
*   **Reporting Service:** Provides analytical insights into order data.

### Data Storage

*   **Order Data:** PostgreSQL (Relational Database)
*   **Inventory Data:** MongoDB (NoSQL Database)

## Setup and Installation

### Prerequisites

*   Docker
*   Kubernetes (for deployment)
*   Google Cloud Platform account (for production deployment)
*   Python 3.9+
*   Poetry (for dependency management, or pipenv/venv)

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/web-todo-app.git
    cd web-todo-app/hotel_order_management_service
    ```

2.  **Set up a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Database Setup:**
    *   **PostgreSQL:** Ensure a PostgreSQL instance is running and accessible. Update `config.py` with your database credentials.
    *   **MongoDB:** Ensure a MongoDB instance is running and accessible. Update `config.py` with your database credentials.

4.  **Run the application:**
    ```bash
    python src/order_management_service/app.py
    ```
    The API will be available at `http://localhost:5000`.

### Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t hotel-order-management-service .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 hotel-order-management-service
    ```

## API Endpoints (Order Management Service)

*   `POST /orders`: Create a new room service order.
*   `GET /orders`: Retrieve a list of all room service orders.
*   `GET /orders/<order_id>`: Retrieve details of a specific room service order.
*   `PUT /orders/<order_id>`: Update an existing room service order.
*   `DELETE /orders/<order_id>`: Cancel a room service order.

## Contributing

Please refer to the `CONTRIBUTING.md` for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License.

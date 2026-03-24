# Web To Do App

This project implements a web-based to-do application with a dummy login and basic to-do functionality, as defined by Jira issue SCRUM-19.

## Table of Contents

- [Project Overview](#project-overview)
- [Technical Stack](#technical-stack)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Running with Docker](#running-with-docker)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [HLD Reference](#hld-reference)

## Project Overview

This application provides a simple, client-side to-do list experience. It includes a simulated login page built with React and styled with Tailwind CSS. After a successful simulated login, users are redirected to the main to-do interface where they can add, mark as done, and delete tasks. All task data is stored locally in the browser's local storage.

## Technical Stack

- **Frontend:** React.js
- **Styling:** Tailwind CSS
- **Containerization (Optional for Development/Deployment):** Docker

## Features

- Dummy login page with Email, Username, and Password fields.
- Simulated authentication and redirection to the to-do list.
- Add new tasks to the list.
- Mark existing tasks as 'done'.
- Delete tasks from the list.
- Client-side data storage using browser's local storage.

## Getting Started

### Prerequisites

- Node.js (version 18 or higher) and npm/yarn
- Git
- Docker (optional, for containerized development/deployment)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/p67428378-afk/web-todo-app.git
   cd web-todo-app
   ```

2. **Install dependencies:**
   ```bash
   yarn install
   # or npm install
   ```

3. **Run the application in development mode:**
   ```bash
   yarn start
   # or npm start
   ```
   The application will be accessible at `http://localhost:3000`.

### Running with Docker

1. **Build the Docker image:**
   ```bash
   docker build -t web-todo-app .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -p 80:80 web-todo-app
   ```
   The application will be accessible at `http://localhost`.

## Project Structure

```
web-todo-app/
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── App.js
│   ├── index.js
│   └── ...
├── Dockerfile
├── package.json
├── README.md
├── tailwind.config.js
└── ...
```

## Deployment

As per the HLD, this is a static React application. It can be deployed to any static site hosting service. The `Dockerfile` provided can be used to build a production-ready image that serves the static files using Nginx.

## HLD Reference

The High-Level Design document for this project can be found [here](https://bfsi-na-ai-engineering.atlassian.net/wiki/spaces/SCRUM1/pages/5767169).

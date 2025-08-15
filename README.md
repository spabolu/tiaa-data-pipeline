# TIAA Data Pipeline Hackathon

Welcome to the TIAA-DataPipeline project! This is a hackathon project that demonstrates the use of AI agents to automate a data processing pipeline. The project is divided into a frontend and a backend, each with its own set of responsibilities.

## Overview

The TIAA-DataPipeline is a full-stack application that showcases how AI can be used to build an intelligent data pipeline. The backend consists of a series of AI-powered agents that work together to ingest, clean, transform, and analyze data. The frontend provides a user-friendly interface for uploading data, monitoring the pipeline's progress, and viewing the results.

## Core Concepts

This project demonstrates several key computer science concepts that are highly relevant in modern software development:

*   **AI Agent-Based Architecture:** The backend is designed around a collection of specialized AI agents. Each agent is responsible for a specific task in the data pipeline (e.g., ingestion, cleaning, transformation). This modular approach makes the system scalable, maintainable, and easy to extend.

*   **Pipeline Orchestration:** The Flask backend acts as an orchestrator, managing the flow of data through the pipeline. It ensures that each agent performs its task in the correct sequence and handles any errors that may occur. This demonstrates a practical application of workflow management and automation.

*   **Full-Stack Development:** The project follows a clear separation of concerns between the frontend and the backend. The React-based frontend is responsible for the user experience, while the Python-based backend handles the business logic and data processing. This is a classic example of a modern full-stack architecture.

*   **Real-Time Communication with WebSockets:** The application uses WebSockets to provide real-time feedback to the user. As the data pipeline progresses through its various stages, the backend sends updates to the frontend, which are then displayed to the user. This creates a dynamic and interactive experience.

## Project Structure

The project is organized into two main directories:

*   `frontend/`: A React-based single-page application that serves as the user interface for the data pipeline.
*   `backend/`: A Python-based Flask application that powers the data processing pipeline and exposes a REST API.

For more detailed information about each component, please refer to their respective `README.md` files:

*   [Frontend README](./frontend/README.md)
*   [Backend README](./backend/README.md)

## Getting Started

To get the entire project up and running, you will need to start both the frontend and backend servers.

### Prerequisites

*   Node.js (v18 or later)
*   Python 3.9 or later
*   pip

### Installation and Setup

1.  **Clone the repository**
    ```sh
    git clone https://github.com/spabolu/tiaa-data-pipeline.git
    cd tiaa-data-pipeline
    ```

2.  **Set up the backend**

    Follow the instructions in the [backend README](./backend/README.md#getting-started) to set up the backend server. This will involve creating a virtual environment, installing the required Python packages, and setting up your environment variables.

3.  **Set up the frontend**

    Follow the instructions in the [frontend README](./frontend/README.md#getting-started) to set up the frontend application. This will involve installing the required npm packages.

### Running the Application

1.  **Start the backend server**

    In a terminal, navigate to the `backend` directory and run the following command:
    ```sh
    source venv/bin/activate
    python app.py
    ```
    The backend server will be running on `http://0.0.0.0:5000`.

2.  **Start the frontend server**

    In a separate terminal, navigate to the `frontend` directory and run the following command:
    ```sh
    npm run dev
    ```
    The frontend application will be available at `http://localhost:5173`.

You can now open your browser and navigate to `http://localhost:5173` to use the application.

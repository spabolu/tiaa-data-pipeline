# TIAA Data Pipeline Hackathon Backend

This is the backend for the TIAA-DataPipeline project. It's a Flask-based application that powers the data processing pipeline and exposes a REST API for the frontend.

## Overview

The backend is responsible for orchestrating a series of AI-powered agents that handle different stages of a data pipeline. It receives data from the frontend, processes it through the pipeline, and stores the results in an AWS RDS database. The backend also uses WebSockets to provide real-time progress updates to the frontend.

## Features

*   **Data Processing Pipeline:** A multi-stage pipeline that ingests, cleans, transforms, and analyzes data.
*   **AI-Powered Agents:** Each stage of the pipeline is handled by a dedicated agent.
*   **REST API:** A set of API endpoints for uploading data, initiating the pipeline, and downloading reports.
*   **WebSocket Communication:** Real-time progress updates are sent to the frontend via WebSockets.
*   **AWS Integration:** The backend uses AWS S3 for file storage and AWS RDS for data persistence.

## Architecture

The backend is organized into the following modules:

*   `app.py`: The main Flask application that defines the API endpoints and manages the pipeline.
*   `pipe/`: Contains the different stages of the data pipeline, with each file representing a specific stage (e.g., `_0ingestion.py`, `_1cleaning.py`).
*   `aws/`: Includes modules for interacting with AWS services like S3 and RDS.
*   `llm/`: Contains the logic for interacting with the AI models that power the pipeline agents.

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

*   Python 3.9 or later
*   pip

### Installation

1.  **Clone the repository**
    ```sh
    git clone https://github.com/spabolu/tiaa-data-pipeline.git
    ```

2.  **Navigate to the backend directory**
    ```sh
    cd tiaa-data-pipeline/backend
    ```

3.  **Create and activate a virtual environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install the required packages**
    ```sh
    pip install -r requirements.txt
    ```

5.  **Set up environment variables**

    Create a `.env.local` file in the `backend` directory and add the following environment variables. These are required for connecting to AWS services.

    ```
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    AWS_SESSION_TOKEN=your_aws_session_token
    AWS_REGION=us-east-1

    DB_HOST=your_db_host
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    DB_PORT=5432
    ```

6.  **Run the Flask application**
    ```sh
    python app.py
    ```

The backend server will be running on `http://0.0.0.0:5000`.

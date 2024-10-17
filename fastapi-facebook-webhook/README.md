# FastAPI Webhook Service

This project is a FastAPI-based webhook service that interacts with Facebook's messaging API and logs incoming webhook data to a MongoDB database.

## Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- `pip` (Python package installer)

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```properties
    VERIFY_TOKEN=<your_verify_token>
    PAGE_ACCESS_TOKEN=<your_page_access_token>
    MONGO_DETAILS=mongodb://user:password@localhost:27017
    ```

## Running the Application

1. **Start MongoDB using Docker Compose:**

    ```sh
    docker-compose up -d
    ```

2. **Run the FastAPI application:**

    ```sh
    uvicorn app.main:app --reload
    ```
## Endpoints

- `GET /messaging-webhook`: Verifies the webhook.
- `POST /messaging-webhook`: Receives and processes incoming webhook data.

# Chatbot Custom Logger FastAPI

A FastAPI application for custom logging 

## Requirements

- Python 3.7+
- MongoDB

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/chatbot-custom-logger-fast-api.git
   cd chatbot-custom-logger-fast-api
2. **Create and activate a virtual environment**:

   - On **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - On **macOS/Linux**:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**:
    ```bash
    pip install -r requirements.txt
4. **Start mongo db with docker compose**
    ```bash
    docker-compose up -d

5. **Run the application**:
     ```bash
    uvicorn app.main:app --reload

    
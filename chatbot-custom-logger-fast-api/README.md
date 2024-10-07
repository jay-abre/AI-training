# Chatbot Custom Logger FastAPI

A FastAPI application for logging chatbot and user events to MongoDB.

## Requirements

- Python 3.7+
- MongoDB

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/chatbot-custom-logger-fast-api.git
   cd chatbot-custom-logger-fast-api
2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    ```bash
    ## On Windows
    venv\Scripts\activate
    (`.\venv\Scripts\activate`)
    ```bash
    ## On macOS/Linux
    source venv/bin/activate
3. **Install dependencies:**:
    ```bash
    pip install -r requirements.txt
4. **Run the application**:
     ```bash
    uvicorn app.main:app --reload
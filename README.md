# Pokemon Search API

A FastAPI backend service that processes Pokemon search queries using OpenAI's GPT-3.5.

## Setup

1. Clone the repository:   ```bash
   git clone <your-repository-url>   ```

2. Navigate to the backend directory:   ```bash
   cd backend   ```

3. Create a virtual environment and activate it:   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate   ```

4. Install dependencies:   ```bash
   pip install -r requirements.txt   ```

5. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

6. Run the server:   ```bash
   python main.py   ```

The server will start at `http://localhost:8880`

## API Endpoints

### POST /api/search
Search for Pokemon information.

Request body:

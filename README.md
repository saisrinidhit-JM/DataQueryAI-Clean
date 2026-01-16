# Data QueryAI

A natural language interface for querying MongoDB databases. Ask questions in plain English and get insights from your data instantly.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React UI      │────▶│   Backend API   │────▶│    MongoDB      │
│   (Frontend)    │     │   (Python)      │     │    Database     │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Gemini AI     │
                        │ (Query + NL Gen)│
                        └─────────────────┘
```

## Features

- **Natural Language Queries**: Ask questions like "How many users are active in the last 10 days?"
- **AI-Powered**: Uses Gemini 2.5 Flash Lite for query generation and response formatting
- **MongoDB Integration**: Direct connection to your MongoDB database
- **Real-time Results**: Instant JSON to natural language conversion

## Project Structure

```
DataQueryAI-Clean/
├── frontend/          # React + Vite + TypeScript UI
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/           # Python FastAPI server
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
└── docs/             # MongoDB schema documentation
```

## Quick Start

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your credentials
python main.py
```

## Environment Variables

Create a `.env` file in the backend folder:

```env
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=your_database_name
```

## How It Works

1. **User Input**: Enter a natural language question in the UI
2. **Query Generation** (Gemini Call 1): AI converts your question to a MongoDB query
3. **Database Query**: Execute the generated query on MongoDB
4. **Response Generation** (Gemini Call 2): AI converts JSON results to natural language
5. **Display**: Results shown in the UI

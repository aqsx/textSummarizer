# Text Summarizer App

A modern web application that provides AI-powered text summarization capabilities. Built with FastAPI, React, and Hugging Face Transformers.

## Features

- Text summarization using state-of-the-art AI models
- Clean and responsive user interface
- Real-time summarization
- Adjustable summary length

## Project Structure

```
textSummarizer/
├── backend/           # FastAPI server
│   ├── app/
│   │   └── main.py
├── frontend/         # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt  # Python dependencies
└── README.md
```

## Setup Instructions

### Backend

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Enter or paste the text you want to summarize
3. Click the "Summarize" button
4. View your summarized text

## Technologies Used

- Backend:
  - FastAPI
  - Hugging Face Transformers
  - PyTorch
  
- Frontend:
  - React
  - TypeScript
  - Chakra UI 
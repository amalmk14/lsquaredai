# Story Generator App
A simple web app that creates short stories about imaginary characters using AI.


## What it does
Add characters with names and descriptions
Generate creative stories about those characters
Clean, simple interface



## Tech Stack

Backend: FastAPI (Python)
Database: Supabase
AI: Google Gemini API
Frontend: HTML + JavaScript



## Setup

### 1. Clone and install

git clone https://github.com/amalmk14/lsquaredai.git
cd storygen
pip install -r requirements.txt


### 2. Environment variables

Create a `.env` file:

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GOOGLE_API_KEY=your_gemini_api_key



### 3. Database setup
Create a table in Supabase:

sql
CREATE TABLE Characters (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  details TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);



### 4. Run the app
uvicorn main:app --reload

Open http://localhost:8000


## API Usage

### Add a character

curl -X POST "http://localhost:8000/api/create_character" \
  -H "Content-Type: application/json" \
  -d '{"name": "Bilbo Baggins", "details": "Hobbit who lives in the Shire with a magic ring"}'


### Generate story

curl -X POST "http://localhost:8000/api/generate_story" \
  -H "Content-Type: application/json" \
  -d '{"character_name": "Bilbo Baggins"}'


## How it works

1. You add characters with their details to the database
2. When you want a story, the app fetches the character info
3. It sends a prompt to Google Gemini AI
4. The AI generates a 4-5 sentence creative story
5. The story gets displayed on the webpage



## Notes

1. Using Gemini 1.5 Flash for better free tier limits
2. Simple error handling for API failures
3. Basic HTML interface focused on functionality over design
4. Stories are generated fresh each time (not stored)

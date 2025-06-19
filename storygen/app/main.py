from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from models import Character, StoryRequest           
from supabase_client import supabase                 # Supabase client to interact with the database
from ai_utils import get_ai_story                    

import os

app = FastAPI()

# Set base directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up Jinja2 template 
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Mount the 'static' files from templates directory
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "templates")), name="static")


@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    # Render and return the index.html 
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/create_character")
def create_character(data: Character):
    try:
        # Insert the character into the Supabase 'Characters' table
        result = supabase.table("Characters").insert({
            "name": data.name,
            "details": data.details
        }).execute()

        # If insert successful, return the new character
        if result.data:
            return result.data[0]
        else:
            raise Exception("Insert failed")

    except Exception as err:
        # Handle error and return 500 response
        print("Insert error:", err)
        raise HTTPException(status_code=500, detail="Could not save character")


@app.get("/api/get_characters")
def get_characters():
    try:
        # Select data from Supabase
        result = supabase.table("Characters").select("id, name, details").execute()
        
        # Return data if available, else return an empty list
        if result.data:
            return result.data
        else:
            return []

    except Exception as err:
        # Handle error and return 500 response
        print("Fetch error:", err)
        raise HTTPException(status_code=500, detail="Could not fetch characters")


@app.post("/api/generate_story")
def generate_story(data: StoryRequest):
    record = None  # Placeholder for the character record

    # If ID is provided, fetch character by ID
    if data.id:
        result = supabase.table("Characters").select("*").eq("id", data.id).execute()

    # If name is provided, fetch character by name
    elif data.character_name:
        result = supabase.table("Characters").select("*").eq("name", data.character_name).execute()

    # If neither provided, raise bad request error
    else:
        raise HTTPException(status_code=400, detail="Need character_name or id")

    # If a matching character is found, assign it to 'record'
    if result.data:
        record = result.data[0]
        print("Character fetched:", record)
    else:
        # Raise 404 if character not found
        raise HTTPException(status_code=404, detail="Character not found")

    # Call Gemini to generate a story using name and details
    story = get_ai_story(record['name'], record['details'])

    # Return the story in JSON format
    return {"story": story}

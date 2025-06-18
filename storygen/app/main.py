from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from models import Character, StoryRequest
from supabase_client import supabase
from ai_utils import get_ai_story
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "templates")), name="static")

class Character(BaseModel):
    name: str
    details: str

class StoryRequest(BaseModel):
    id: int = None
    character_name: str = None

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/create_character")
def create_character(data: Character):
    try:
        result = supabase.table("Characters").insert({
            "name": data.name,
            "details": data.details
        }).execute()

        if result.data:
            return result.data[0]
        else:
            raise Exception("Insert failed")
    except Exception as err:
        print("Insert error:", err)
        raise HTTPException(status_code=500, detail="Could not save character")
    

@app.get("/api/get_characters")
def get_characters():
    try:
        result = supabase.table("Characters").select("id, name, details").execute()
        
        if result.data:
            return result.data
        else:
            return []
    except Exception as err:
        print("Fetch error:", err)
        raise HTTPException(status_code=500, detail="Could not fetch characters")

@app.post("/api/generate_story")
def generate_story(data: StoryRequest):
    record = None

    if data.id:
        result = supabase.table("Characters").select("*").eq("id", data.id).execute()
    elif data.character_name:
        result = supabase.table("Characters").select("*").eq("name", data.character_name).execute()
    else:
        raise HTTPException(status_code=400, detail="Need character_name or id")

    if result.data:
        record = result.data[0]
        print(" Character fetched:", record)
    else:
        raise HTTPException(status_code=404, detail="Character not found")

    story = get_ai_story(record['name'], record['details'])
    return {"story": story}



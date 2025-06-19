from pydantic import BaseModel  # For data validation
from typing import Optional     # For optional fields

class Character(BaseModel):
    name: str       # Character name
    details: str    # Character description

class StoryRequest(BaseModel):
    id: Optional[int] = None             # Optional story ID
    character_name: Optional[str] = None # Optional character name

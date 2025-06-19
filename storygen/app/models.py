from pydantic import BaseModel  
from typing import Optional    

class Character(BaseModel):
    name: str       
    details: str    

class StoryRequest(BaseModel):
    id: Optional[int] = None             
    character_name: Optional[str] = None 

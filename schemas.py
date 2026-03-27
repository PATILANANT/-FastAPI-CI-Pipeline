from pydantic import BaseModel
from typing import List, Optional

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []

class Note(NoteCreate):
    id: int
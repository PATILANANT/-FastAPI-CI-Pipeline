from fastapi import FastAPI, Depends, HTTPException
from typing import List
from models import notes_db
from schemas import NoteCreate, Note
from auth import get_current_user

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Notes API Running 🚀"}

@app.post("/notes", response_model=Note)
def create_note(note: NoteCreate, user=Depends(get_current_user)):
    note_id = len(notes_db) + 1
    new_note = {"id": note_id, **note.dict()}
    notes_db.append(new_note)
    return new_note


@app.get("/notes", response_model=List[Note])
def get_notes(skip: int = 0, limit: int = 10):
    return notes_db[skip: skip + limit]


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes_db:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: NoteCreate):
    for note in notes_db:
        if note["id"] == note_id:
            note.update(updated_note.dict())
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    global notes_db
    notes_db = [n for n in notes_db if n["id"] != note_id]
    return {"message": "Deleted successfully"}

@app.get("/search")
def search_notes(query: str):
    return [
        note for note in notes_db
        if query.lower() in note["title"].lower()
        or query.lower() in note["content"].lower()
    ]

@app.get("/filter")
def filter_by_tag(tag: str):
    return [note for note in notes_db if tag in note["tags"]]
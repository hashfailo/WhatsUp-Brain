from fastapi import FastAPI
from app.schemas import NoteCreate
from app.database import engine
from app.models import Base
from app.database import SessionLocal
from app.models import Note
from fastapi import HTTPException

app = FastAPI(
    title="WhatsUp Brain API",
    description="A tiny REST API for storing notes",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

@app.post("/notes")
def create_note(note: NoteCreate):
    db = SessionLocal()
    db_note = Note(content=note.content)

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    db.close()
    return {
        "id": db_note.id,
        "note": db_note.content
    }

@app.get("/notes")
def read_notes():
    db = SessionLocal()
    notes = db.query(Note).all()

    db.close()
    return [
        {
            "id": note.id,
            "note": note.content
        }
        for note in notes
    ]

@app.get("/notes/{id}")
def read_note(id: int):
    db = SessionLocal()

    note = db.query(Note).filter(Note.id == id).first()
    db.close()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found brotherr!"
        )
    
    return {
        "id": note.id,
        "note": note.content
    }

@app.delete("/notes/{id}")
def delete_note(id: int):
    db = SessionLocal()

    note = db.query(Note).filter(Note.id == id).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note to be deleted isn't found brooo!"
        )
    
    db.delete(note)
    db.commit()
    db.close()

    return {
        "message": "Note deleted successfully."
    }
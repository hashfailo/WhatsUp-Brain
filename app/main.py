from fastapi import FastAPI
from app.schemas import NoteCreate
from app.database import engine
from app.models import Base
from app.database import SessionLocal
from app.models import Note

app = FastAPI()
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

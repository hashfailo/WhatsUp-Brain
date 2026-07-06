# this file describes what the api accepts/returns.

from pydantic import BaseModel

class NoteCreate(BaseModel):
    content: str
# app/schemas/impressao_schema.py

from pydantic import BaseModel

class InstrutorNome(BaseModel):
    instrutor: str

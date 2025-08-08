from pydantic import BaseModel
from typing import Optional

class InstrutorCreate(BaseModel):
    instrutor: str
    link_zoom: str
    espanhol: bool
    portugues: bool
    ingles: bool
    frances: bool
    japones: bool
    italiano: bool
    senha: Optional[str] = None
    funcao: str
    colina: Optional[int] = 0
    supervisor: Optional[str] = None  # 👈 String, já que no banco é VARCHAR

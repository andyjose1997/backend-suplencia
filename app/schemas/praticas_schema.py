from typing import Optional
from pydantic import BaseModel

class PraticaAtualizacao(BaseModel):
    id: str
    turno: str
    tipo: str

    # Campos da prática A
    instrutor_A: Optional[str] = None
    link_A: Optional[str] = None
    sala_A: Optional[str] = None
    horario_A: Optional[str] = None
    idioma_A: Optional[str] = None
    disponibilidade_A: Optional[str] = None
    subs_A: Optional[int] = None

    # Campos da prática B
    instrutor_B: Optional[str] = None
    link_B: Optional[str] = None
    sala_B: Optional[str] = None
    horario_B: Optional[str] = None
    idioma_B: Optional[str] = None
    disponibilidade_B: Optional[str] = None
    subs_B: Optional[int] = None

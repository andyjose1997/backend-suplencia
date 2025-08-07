from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.models import Instrutor
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

@router.get("/nomes_tabelas")
def listar_nomes_tabelas(db: Session = Depends(get_db)):
    try:
        resultado = db.execute(text("SHOW TABLES"))
        nomes = [linha[0] for linha in resultado]
        return nomes
    except Exception as e:
        print("❌ ERRO AO CONSULTAR O BANCO:", e)
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel
from typing import Optional

class InstrutorUpdate(BaseModel):
    instrutor: str
    link_zoom: str
    ingles: Optional[bool] = False
    espanhol: Optional[bool] = False
    portugues: Optional[bool] = False
    frances: Optional[bool] = False
    japones: Optional[bool] = False
    italiano: Optional[bool] = False


@router.put("/editar_instrutor/{id}")
def editar_instrutor(id: str, dados: InstrutorUpdate, db: Session = Depends(get_db)):
    print("📤 DADOS PARA UPDATE:", dados.dict())

    instrutor = db.query(Instrutor).filter(Instrutor.id == id).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    for campo, valor in dados.dict().items():
        setattr(instrutor, campo, valor)

    print("💾 Aplicando:", {
        "ingles": instrutor.ingles,
        "espanhol": instrutor.espanhol,
        "portugues": instrutor.portugues,
        "frances": instrutor.frances,
        "japones": instrutor.japones,
        "italiano": instrutor.italiano,
    })

    db.commit()
    return {"mensagem": "Atualizado com sucesso"}


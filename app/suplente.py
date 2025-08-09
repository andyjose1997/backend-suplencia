from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import SuplenteAtual
from pydantic import BaseModel
import uuid

router = APIRouter()

# ✅ Schema para entrada
class SuplenteEntrada(BaseModel):
    nome: str

# ✅ Buscar suplente atual
@router.get("/suplente_atual")
def get_suplente(db: Session = Depends(get_db)):
    suplente = db.query(SuplenteAtual).first()
    return suplente

# ✅ Definir novo suplente (sempre substitui)
@router.post("/suplente_atual")
def set_suplente(dados: SuplenteEntrada, db: Session = Depends(get_db)):
    # Apaga o suplente atual, se existir
    existente = db.query(SuplenteAtual).first()
    if existente:
        db.delete(existente)
        db.commit()

    # Adiciona o novo suplente
    novo = SuplenteAtual(id=str(uuid.uuid4()), instrutor=dados.nome)
    db.add(novo)
    db.commit()
    return {"mensagem": f"{dados.nome} agora é o suplente atual"}

@router.post("/suplente_atual")
def set_suplente(dados: SuplenteEntrada, db: Session = Depends(get_db)):
    existente = db.query(SuplenteAtual).first()
    if existente:
        db.delete(existente)
        db.commit()

    novo = SuplenteAtual(id=str(uuid.uuid4()), instrutor=dados.nome)
    db.add(novo)
    db.commit()

    # ✅ Retorna o suplente com o nome
    return {"instrutor": novo.instrutor}

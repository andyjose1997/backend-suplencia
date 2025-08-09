from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import SuplenteAtual
from pydantic import BaseModel
import uuid

router = APIRouter()

class SuplenteEntrada(BaseModel):
    nome: str

# 🔹 Buscar suplente atual
@router.get("/suplente_atual")
def get_suplente(db: Session = Depends(get_db)):
    suplente = db.query(SuplenteAtual).first()
    if not suplente:
        return {}
    return {"instrutor": suplente.instrutor}

# 🔹 Definir novo suplente
@router.post("/suplente_atual")
def set_suplente(dados: SuplenteEntrada, db: Session = Depends(get_db)):
    if not dados.nome or not dados.nome.strip():
        raise HTTPException(status_code=400, detail="Nome do suplente não pode ser vazio.")

    # Remove suplente atual, se existir
    existente = db.query(SuplenteAtual).first()
    if existente:
        db.delete(existente)
        db.commit()

    # Adiciona novo suplente
    novo = SuplenteAtual(id=str(uuid.uuid4()), instrutor=dados.nome.strip())
    db.add(novo)
    db.commit()

    return {"instrutor": dados.nome.strip()}

@router.post("/suplente_atual")
def set_suplente(dados: SuplenteEntrada, db: Session = Depends(get_db)):
    if not dados.nome or not dados.nome.strip():
        raise HTTPException(status_code=400, detail="Nome do suplente não pode ser vazio.")

    existente = db.query(SuplenteAtual).first()

    if existente:
        existente.instrutor = dados.nome.strip()
    else:
        novo = SuplenteAtual(id=str(uuid.uuid4()), instrutor=dados.nome.strip())
        db.add(novo)

    db.commit()

    return {"mensagem": f"{dados.nome} agora é o suplente atual"}

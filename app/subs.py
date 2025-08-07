from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor
from pydantic import BaseModel

router = APIRouter()

# GET todos os instrutores
@router.get("/instrutores")
def listar_instrutores(db: Session = Depends(get_db)):
    return db.query(Instrutor).all()

# GET apenas os SUBs
@router.get("/subs")
def listar_subs(db: Session = Depends(get_db)):
    return db.query(Instrutor).filter(Instrutor.sub == 1).all()

# POST marca sub = 1
@router.post("/marcar_sub/{id}")
def marcar_como_sub(id: str, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.id == id).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")
    instrutor.sub = 1
    db.add(instrutor)
    db.commit()
    return {"mensagem": f"{instrutor.instrutor} marcado como SUB"}

# POST marca sub = 0
@router.post("/desmarcar_sub/{id}")
def desmarcar_como_sub(id: str, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.id == id).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")
    instrutor.sub = 0
    db.add(instrutor)
    db.commit()
    return {"mensagem": f"{instrutor.instrutor} removido da lista SUB"}

# PUT atualiza o campo "ate"
class AteEntrada(BaseModel):
    id: str
    ate: str

@router.put("/atualizar_ate")
def atualizar_ate(dados: AteEntrada, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.id == dados.id).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")
    instrutor.ate = dados.ate
    db.add(instrutor)
    db.commit()
    return {"mensagem": "Horário atualizado com sucesso"}

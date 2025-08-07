from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.models import Instrutor
from pydantic import BaseModel

router = APIRouter()

@router.get("/nomes_tabelas")
def listar_nomes_tabelas():
    return ["instrutores"]

@router.get("/visualizar_tabela/{nome}")
def visualizar_tabela(nome: str, db: Session = Depends(get_db)):
    dados = db.execute(text(f"SELECT * FROM `{nome}`"))
    colunas = dados.keys()
    registros = [dict(zip(colunas, linha)) for linha in dados.fetchall()]
    return registros
    
@router.delete("/apagar_instrutor/{id}")
def apagar_instrutor(id: str, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.id == id).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")
    db.delete(instrutor)
    db.commit()
    return {"mensagem": "Instrutor apagado com sucesso"}

# ✅ NOVO: modelo para edição
class InstrutorEdicao(BaseModel):
    instrutor: str
    link_zoom: str | None = None
    funcao: str

@router.put("/editar_instrutor/{id}")
def editar_instrutor(id: int, dados: InstrutorEdicao, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.id == id).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    instrutor.instrutor = dados.instrutor
    instrutor.link_zoom = dados.link_zoom
    instrutor.funcao = dados.funcao

    db.commit()
    return {"mensagem": "Instrutor atualizado com sucesso"}

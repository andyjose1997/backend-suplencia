from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor
from pydantic import BaseModel

router = APIRouter()

class TrocaSenhaEntrada(BaseModel):
    instrutor: str
    senha_atual: str
    nova_senha: str

@router.put("/trocar-senha")
def trocar_senha(dados: TrocaSenhaEntrada, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.instrutor == dados.instrutor).first()

    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado.")

    if dados.senha_atual != instrutor.senha:
        raise HTTPException(status_code=401, detail="Senha atual incorreta.")

    instrutor.senha = dados.nova_senha
    db.commit()

    return {"mensagem": "Senha atualizada com sucesso."}

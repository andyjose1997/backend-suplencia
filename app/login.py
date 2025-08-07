from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor
from app.auth import criar_token_acesso
from pydantic import BaseModel

router = APIRouter()

class LoginData(BaseModel):
    instrutor: str
    senha: str

@router.post("/login")
def login(dados: LoginData, db: Session = Depends(get_db)):
    usuario = db.query(Instrutor).filter(Instrutor.instrutor == dados.instrutor).first()

    if not usuario or dados.senha != usuario.senha:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token_acesso({
        "sub": usuario.instrutor,
        "funcao": usuario.funcao,
        "instrutor": usuario.instrutor
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "instrutor_nome": usuario.instrutor  # ✅ Nome real do banco
    }

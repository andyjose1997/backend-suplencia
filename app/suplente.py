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

# ✅ Definir ou atualizar suplente
@router.post("/suplente_atual")
def set_suplente(dados: SuplenteEntrada, db: Session = Depends(get_db)):
    try:
        # Impede nome vazio ou só espaços
        if not dados.nome or not dados.nome.strip():
            raise HTTPException(status_code=400, detail="Nome do suplente não pode ser vazio.")

        # Se já existir suplente, apenas atualiza
        existente = db.query(SuplenteAtual).first()
        if existente:
            existente.instrutor = dados.nome
        else:
            # Cria novo registro
            existente = SuplenteAtual(id=str(uuid.uuid4()), instrutor=dados.nome)
            db.add(existente)

        db.commit()
        return novo  # se for o objeto do SQLAlchemy com instrutor e id

    except HTTPException:
        raise
    except Exception as e:
        # Retorna erro genérico sem quebrar CORS
        return {"erro": str(e)}
@router.post("/suplente_atual")
def set_suplente(dados: SuplenteEntrada, db: Session = Depends(get_db)):
    existente = db.query(SuplenteAtual).first()
    if existente:
        db.delete(existente)
        db.commit()

    novo = SuplenteAtual(id=str(uuid.uuid4()), instrutor=dados.nome)
    db.add(novo)
    db.commit()

    return {"instrutor": dados.nome}  # ✅ React vai conseguir exibir

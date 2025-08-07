from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Anuncio
from pydantic import BaseModel

router = APIRouter()

class AnuncioEntrada(BaseModel):
    conteudo: str

@router.post("/anuncios")
def criar_anuncio(dados: AnuncioEntrada, db: Session = Depends(get_db)):
    if not dados.conteudo.strip():
        raise HTTPException(status_code=400, detail="Conteúdo obrigatório")
    novo = Anuncio(conteudo=dados.conteudo.strip())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/anuncios")
def listar_anuncios(db: Session = Depends(get_db)):
    return db.query(Anuncio).order_by(Anuncio.id.desc()).all()

@router.put("/anuncios/{anuncio_id}")
def editar_anuncio(anuncio_id: int, dados: AnuncioEntrada, db: Session = Depends(get_db)):
    anuncio = db.query(Anuncio).filter(Anuncio.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")
    anuncio.conteudo = dados.conteudo.strip()
    db.commit()
    return anuncio

@router.delete("/anuncios/{anuncio_id}")
def apagar_anuncio(anuncio_id: int, db: Session = Depends(get_db)):
    anuncio = db.query(Anuncio).filter(Anuncio.id == anuncio_id).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")
    db.delete(anuncio)
    db.commit()
    return {"mensagem": "Anúncio deletado"}

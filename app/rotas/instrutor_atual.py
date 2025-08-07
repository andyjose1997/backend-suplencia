from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Instrutor

router = APIRouter()

@router.get("/instrutor/{nome}")
def buscar_instrutor_por_nome(nome: str, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(func.lower(Instrutor.instrutor) == nome.lower()).first()

    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    return {
        "instrutor": instrutor.instrutor,
        "link_zoom": instrutor.link_zoom or ""
    }

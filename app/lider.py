from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor

router = APIRouter()

@router.get("/lider")
def obter_lider(db: Session = Depends(get_db)):
    try:
        print("🔍 Buscando líder...")
        lider = db.query(Instrutor).filter(Instrutor.colina == 1).first()
        print("✅ Resultado da consulta:", lider)

        if lider is None:
            return {"nome": None}

        if not hasattr(lider, "instrutor"):
            raise HTTPException(status_code=500, detail="Campo 'instrutor' não encontrado no líder")

        return {"nome": lider.instrutor}

    except Exception as e:
        print("❌ ERRO CAPTURADO:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

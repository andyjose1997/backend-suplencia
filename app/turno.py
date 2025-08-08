from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import text
from pydantic import BaseModel

router = APIRouter()

class TurnoUpdate(BaseModel):
    novo_turno: str

@router.get("/turno")
def get_turno(db: Session = Depends(get_db)):
    try:
        resultado = db.execute(text("SELECT DISTINCT turno FROM instrutores LIMIT 1")).fetchone()
        return {"turno": resultado[0] if resultado else "manha"}
    except Exception as e:
        return {"erro": str(e)}

@router.post("/turno")
def set_turno(payload: TurnoUpdate, db: Session = Depends(get_db)):
    if payload.novo_turno not in ["manha", "tarde", "noite"]:
        raise HTTPException(status_code=400, detail="Turno inválido")
    try:
        db.execute(text("UPDATE instrutores SET turno = :t"), {"t": payload.novo_turno})
        db.commit()
        return {"mensagem": f"Turno atualizado para {payload.novo_turno}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/turno-atual")
def get_turno_atual(db: Session = Depends(get_db)):
    try:
        resultado = db.execute(text("SELECT DISTINCT turno FROM instrutores LIMIT 1")).fetchone()
        return {"turno": resultado[0] if resultado else "manha"}
    except Exception as e:
        return {"erro": str(e)}

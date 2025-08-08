# app/visualizarsuper.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor

router = APIRouter()

@router.get("/debug-supervisores")
def debug_supervisores(db: Session = Depends(get_db)):
    instrutores = db.query(Instrutor).all()
    return [{"instrutor": i.instrutor, "supervisor": i.supervisor} for i in instrutores]

# opcional: retorna só o usuário logado (se você tiver auth por token)
# from app.auth import get_current_user
# @router.get("/me/supervisor")
# def me_supervisor(user=Depends(get_current_user), db: Session = Depends(get_db)):
#     i = db.query(Instrutor).filter(Instrutor.instrutor == user.instrutor).first()
#     if not i:
#         raise HTTPException(status_code=404, detail="Perfil não encontrado")
#     return {"instrutor": i.instrutor, "supervisor": i.supervisor}

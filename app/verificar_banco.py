# app/verificar_banco.py
from fastapi import APIRouter, Depends
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/verificar-banco")
def verificar_banco(db: Session = Depends(get_db)):
    inspetor = inspect(db.bind)
    resultado = {}

    for tabela in inspetor.get_table_names():
        colunas = [coluna["name"] for coluna in inspetor.get_columns(tabela)]
        resultado[tabela] = colunas

    return resultado

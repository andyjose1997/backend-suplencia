from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

@router.get("/testar-banco")
def testar_banco(db: Session = Depends(get_db)):
    try:
        # 📄 Busca todas as tabelas
        tabelas_resultado = db.execute(text("SHOW TABLES")).fetchall()
        tabelas = [linha[0] for linha in tabelas_resultado]

        estrutura = {}
        # 📑 Busca colunas de cada tabela
        for tabela in tabelas:
            colunas_resultado = db.execute(text(f"SHOW COLUMNS FROM {tabela}")).fetchall()
            colunas = [coluna[0] for coluna in colunas_resultado]
            estrutura[tabela] = colunas

        return estrutura
    except Exception as e:
        return {"erro": str(e)}

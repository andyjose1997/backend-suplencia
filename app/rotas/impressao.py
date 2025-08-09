from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models import Impressao, Instrutor
from app.schemas.impressao_schema import InstrutorNome  # ✅ import correto

router = APIRouter()

# ✅ Modelo Pydantic para entrada de dados
class ImpressaoEntrada(BaseModel):
    sala: str
    instrutor: str
    pode_imprimir: bool
    faltou: Optional[bool] = None
    observacoes: str = ""
    entregue: Optional[bool] = False

# ✅ POST /impressao
@router.post("/impressao")
def salvar_impressao(dados: ImpressaoEntrada, db: Session = Depends(get_db)):
    try:
        nova = Impressao(
            sala=dados.sala,
            instrutor=dados.instrutor,
            pode_imprimir=dados.pode_imprimir,
            faltou=dados.faltou if dados.faltou is not None else False,
            observacoes=dados.observacoes,
            entregue=dados.entregue if dados.entregue is not None else False
        )
        db.add(nova)
        db.commit()
        db.refresh(nova)
        return {"mensagem": "Registro salvo com sucesso", "id": nova.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar: {e}")

# ✅ GET /impressoes
@router.get("/impressoes")
def listar_impressoes(db: Session = Depends(get_db)):
    try:
        registros = db.query(Impressao).order_by(Impressao.id.desc()).all()
        return [
            {
                "id": r.id,
                "sala": r.sala,
                "instrutor": r.instrutor,
                "pode_imprimir": r.pode_imprimir,
                "faltou": r.faltou,
                "observacoes": r.observacoes,
                "entregue": r.entregue
            }
            for r in registros
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar impressões: {e}")

# ✅ PUT /impressao/{id}
@router.put("/impressao/{id}")
def atualizar_impressao(id: int, dados: ImpressaoEntrada, db: Session = Depends(get_db)):
    registro = db.query(Impressao).filter(Impressao.id == id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    try:
        registro.sala = dados.sala
        registro.instrutor = dados.instrutor
        registro.pode_imprimir = dados.pode_imprimir
        registro.faltou = dados.faltou if dados.faltou is not None else False
        registro.observacoes = dados.observacoes
        registro.entregue = dados.entregue if dados.entregue is not None else False

        db.commit()
        db.refresh(registro)
        return {"mensagem": "Registro atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {e}")

# ✅ DELETE /impressao/tudo
@router.delete("/impressao/tudo")
async def apagar_todos(request: Request, db: Session = Depends(get_db)):
    try:
        db.query(Impressao).delete()
        db.commit()
        return {"mensagem": "Todos os registros foram apagados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao apagar todos: {e}")

# ✅ DELETE /impressao/{id}
@router.delete("/impressao/{id}")
def apagar_impressao(id: int, db: Session = Depends(get_db)):
    registro = db.query(Impressao).filter(Impressao.id == id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    try:
        db.delete(registro)
        db.commit()
        return {"mensagem": "Registro apagado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao apagar: {e}")

# ✅ POST /definir-encarregado-impressao
@router.post("/definir-encarregado-impressao")
def definir_encarregado(dados: InstrutorNome, db: Session = Depends(get_db)):
    try:
        print("📥 Dados recebidos:", dados)
        instrutor_nome = dados.instrutor

        # Zera todos
        db.query(Instrutor).update({Instrutor.coluna_impressao: 0})
        db.commit()

        # Define o novo encarregado
        instrutor = db.query(Instrutor).filter(Instrutor.instrutor == instrutor_nome).first()
        if not instrutor:
            print("❌ Instrutor não encontrado:", instrutor_nome)
            raise HTTPException(status_code=404, detail="Instrutor não encontrado")

        instrutor.coluna_impressao = 1
        db.commit()

        print("✅ Encarregado definido com sucesso:", instrutor_nome)
        return {"mensagem": "Encarregado definido com sucesso"}
    except Exception as e:
        print("❌ ERRO INTERNO:", e)
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")

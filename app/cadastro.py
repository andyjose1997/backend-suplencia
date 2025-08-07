from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor
from app.schemas import InstrutorCreate
import uuid

router = APIRouter()

# ✅ ROTA DE CADASTRO
@router.post("/cadastro")
def cadastrar_instrutor(dados: InstrutorCreate, db: Session = Depends(get_db)):
    print("📥 Dados recebidos:", dados.dict())

    instrutor_existente = db.query(Instrutor).filter(Instrutor.instrutor == dados.instrutor).first()
    if instrutor_existente:
        print("⚠️ Já existe instrutor:", instrutor_existente.instrutor)
        raise HTTPException(status_code=400, detail="Instrutor já cadastrado")

    try:
        senha = dados.senha  # texto puro
        print("🔐 Senha recebida diretamente (sem hash)")
    except Exception as e:
        print("❌ Erro ao obter senha:", e)
        raise HTTPException(status_code=500, detail="Erro ao processar senha")

    try:
        novo_instrutor = Instrutor(
    id=str(uuid.uuid4())[:8],
    instrutor=dados.instrutor,
    link_zoom=dados.link_zoom,
    espanhol=dados.espanhol,
    portugues=dados.portugues,
    ingles=dados.ingles,
    frances=dados.frances,
    japones=dados.japones,
    italiano=dados.italiano,
    senha=senha,
    funcao=dados.funcao,
    colina=dados.colina  # ✅ adicione esta linha
)


        db.add(novo_instrutor)
        db.commit()
        db.refresh(novo_instrutor)
        print("✅ Cadastro realizado com sucesso")
        return {"mensagem": "Instrutor cadastrado com sucesso!", "id": novo_instrutor.id}

    except Exception as e:
        print("❌ ERRO AO SALVAR NO BANCO:", e)
        raise HTTPException(status_code=500, detail="Erro interno ao salvar no banco")


# ✅ ROTA DE EDIÇÃO
@router.put("/editar_instrutor/{id}")
def editar_instrutor(id: str, dados: InstrutorCreate, db: Session = Depends(get_db)):
    print("✏️ Solicitada edição do instrutor ID:", id)
    instrutor = db.query(Instrutor).filter(Instrutor.id == id).first()

    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    try:
        instrutor.instrutor = dados.instrutor
        instrutor.link_zoom = dados.link_zoom
        instrutor.funcao = dados.funcao
        instrutor.portugues = dados.portugues
        instrutor.espanhol = dados.espanhol
        instrutor.ingles = dados.ingles
        instrutor.frances = dados.frances
        instrutor.japones = dados.japones
        instrutor.italiano = dados.italiano
        instrutor.colina = dados.colina  # ✅ adicione isto

        if dados.senha and dados.senha.strip() != "":
            instrutor.senha = dados.senha  # texto puro

        db.commit()
        db.refresh(instrutor)
        print("✅ Instrutor atualizado com sucesso")
        return {"mensagem": "Atualizado com sucesso"}

    except Exception as e:
        print("❌ ERRO AO ATUALIZAR:", e)
        raise HTTPException(status_code=500, detail="Erro ao atualizar instrutor")
@router.get("/instrutor/{nome}")
def obter_instrutor_por_nome(nome: str, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.instrutor == nome).first()

    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    return {
        "id": instrutor.id,
        "instrutor": instrutor.instrutor,
        "link_zoom": instrutor.link_zoom,
        "funcao": instrutor.funcao,
        "portugues": instrutor.portugues,
        "espanhol": instrutor.espanhol,
        "ingles": instrutor.ingles,
        "frances": instrutor.frances,
        "japones": instrutor.japones,
        "italiano": instrutor.italiano,
        "senha": instrutor.senha,  # apenas para testes — pode remover
    }


    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    return {
        "id": instrutor.id,
        "instrutor": instrutor.instrutor,
        "link_zoom": instrutor.link_zoom,
        "funcao": instrutor.funcao,
        "portugues": instrutor.portugues,
        "espanhol": instrutor.espanhol,
        "ingles": instrutor.ingles,
        "frances": instrutor.frances,
        "japones": instrutor.japones,
        "italiano": instrutor.italiano,
        "senha": instrutor.senha,  # só para teste — pode remover depois
    }

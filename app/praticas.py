from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor, PraticaGeral
from app.schemas.praticas_schema import PraticaAtualizacao
from pydantic import BaseModel

router = APIRouter()

# ✅ Schema para edição de instrutor
class InstrutorEntrada(BaseModel):
    instrutor: str
    senha: str | None = None
    link_zoom: str
    funcao: str
    portugues: bool
    espanhol: bool
    ingles: bool
    frances: bool
    japones: bool
    italiano: bool

# ✅ Listar todos os instrutores
@router.get("/instrutores", response_model=None)
def listar_instrutores(db: Session = Depends(get_db)):
    return db.query(Instrutor).all()

# ✅ Definir líder
@router.post("/definir-lider/{id_instrutor}")
def definir_lider(id_instrutor: str, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.id == id_instrutor).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    db.query(Instrutor).update({Instrutor.colina: 0})
    instrutor.colina = 1
    db.commit()
    return {"mensagem": f"{instrutor.instrutor} agora é o líder"}

# ✅ Remover líder
@router.post("/remover-lider/{id_instrutor}")
def remover_lider(id_instrutor: int, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.id == id_instrutor).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    instrutor.colina = 0
    db.commit()
    return {"mensagem": f"{instrutor.instrutor} não é mais líder"}

# ✅ Listar práticas por turno
@router.get("/praticas")
def listar_praticas(turno: str, db: Session = Depends(get_db)):
    try:
        praticas = db.query(PraticaGeral).filter(PraticaGeral.turno == turno).all()
        resultado = []
        for p in praticas:
            p_dict = p.__dict__.copy()
            p_dict.pop("_sa_instance_state", None)
            resultado.append(p_dict)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Atualizar prática A ou B
@router.post("/praticas/atualizar")
async def atualizar_pratica(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    print("📦 RECEBIDO PURO:", body.decode())

    try:
        dados = PraticaAtualizacao.parse_raw(body)
        dados_dict = dados.dict()
        print("📥 DADOS VÁLIDOS:", dados_dict)

        id_alvo = dados_dict["id"]
        pratica = db.query(PraticaGeral).filter(PraticaGeral.id == id_alvo).first()

        if not pratica:
            raise HTTPException(status_code=404, detail="Registro não encontrado")

        for campo, valor in dados_dict.items():
            if campo == "id":
                continue
            print(f"🧪 Campo: {campo} => {valor}")
            try:
                if hasattr(pratica, campo):
                    setattr(pratica, campo, valor)
                else:
                    print(f"⚠️ Campo ignorado (não existe no modelo): {campo}")
            except Exception as e:
                print(f"❌ Erro ao aplicar o campo '{campo}': {e}")

        db.commit()
        return {"mensagem": "Prática atualizada com sucesso."}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ✅ Editar instrutor
@router.put("/editar_instrutor/{id}")
def editar_instrutor(id: str, dados: InstrutorEntrada, db: Session = Depends(get_db)):
    instrutor = db.query(Instrutor).filter(Instrutor.id == id).first()
    if not instrutor:
        raise HTTPException(status_code=404, detail="Instrutor não encontrado")

    instrutor.instrutor = dados.instrutor
    instrutor.link_zoom = dados.link_zoom
    instrutor.funcao = dados.funcao
    instrutor.portugues = dados.portugues
    instrutor.espanhol = dados.espanhol
    instrutor.ingles = dados.ingles
    instrutor.frances = dados.frances
    instrutor.japones = dados.japones
    instrutor.italiano = dados.italiano

    if dados.senha:
        instrutor.senha = dados.senha

    db.commit()
    db.refresh(instrutor)
    return {"mensagem": "Atualizado com sucesso"}

# ✅ Apagar práticas de um turno
@router.delete("/praticas/apagar-turno/{turno}")
def apagar_praticas_turno(turno: str, db: Session = Depends(get_db)):
    try:
        praticas = db.query(PraticaGeral).filter(PraticaGeral.turno == turno).all()

        for p in praticas:
            if p.tipo == "A":
                p.instrutor_A = None
                p.link_A = None
                p.sala_A = None
                p.horario_A = None
                p.idioma_A = None
                p.subs_A = None
            if p.tipo == "B":
                p.instrutor_B = None
                p.link_B = None
                p.sala_B = None
                p.horario_B = None
                p.idioma_B = None
                p.subs_B = None

        db.commit()
        return {"mensagem": f"Todas as práticas do turno '{turno}' foram apagadas com sucesso."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao apagar práticas: {str(e)}")

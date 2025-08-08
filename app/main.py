from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import Base, engine, get_db
from app.models import Instrutor

app = FastAPI()

Base.metadata.create_all(bind=engine)

origens_permitidas = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://suplencia-ctm.vercel.app", 

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← para teste
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"mensagem": "API de Informações está ativa!"}

# ✅ SUA NOVA ROTA DE TESTE DE CONEXÃO
@app.get("/testar-banco")
def testar_conexao(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "✅ Conectado ao banco de dados"}
    except Exception as e:
        return {"status": "❌ Erro ao conectar", "detalhe": str(e)}

# Rotas
from app import login, cadastro, visualizar, nome_tabelas, praticas, upload_foto, turno, lider, subs, quantos, anuncios, suplente, senha
from app.rotas import instrutor_atual, impressao

app.include_router(login.router)
app.include_router(cadastro.router)
app.include_router(visualizar.router)
app.include_router(nome_tabelas.router)
app.include_router(praticas.router)
app.include_router(upload_foto.router)
app.include_router(turno.router)
app.include_router(lider.router)
app.include_router(instrutor_atual.router)
app.include_router(impressao.router)
app.include_router(subs.router)
app.include_router(quantos.router)
app.include_router(anuncios.router)
app.include_router(suplente.router)
app.include_router(senha.router)
from app import visualizarsuper 

app.include_router(visualizarsuper.router) 

# Arquivos estáticos
app.mount("/fotos", StaticFiles(directory="app/fotos"), name="fotos")
from app import verificar_banco
app.include_router(verificar_banco.router)

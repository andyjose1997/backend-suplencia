from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import Base, engine, get_db
from app.models import Instrutor

app = FastAPI()

# Criar as tabelas no banco, se não existirem
Base.metadata.create_all(bind=engine)

# ✅ Lista de origens permitidas
origens_permitidas = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://suplencia-ctm.vercel.app",
    "https://backend-suplencia.onrender.com"
]

# ✅ Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"mensagem": "API de Informações está ativa!"}

# ✅ Rota de teste de conexão com o banco
@app.get("/testar-banco")
def testar_conexao(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "✅ Conectado ao banco de dados"}
    except Exception as e:
        return {"status": "❌ Erro ao conectar", "detalhe": str(e)}

# ✅ Importação e inclusão de rotas
from app import (
    login, cadastro, visualizar, nome_tabelas, praticas, upload_foto,
    turno, lider, subs, quantos, anuncios, suplente, senha, visualizarsuper, verificar_banco
)
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
app.include_router(visualizarsuper.router)
app.include_router(verificar_banco.router)

# ✅ Arquivos estáticos (imagens de perfil, etc.)
app.mount("/fotos", StaticFiles(directory="app/fotos"), name="fotos")

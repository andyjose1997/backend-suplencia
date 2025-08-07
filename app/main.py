from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import Instrutor

app = FastAPI()

Base.metadata.create_all(bind=engine)

origens_permitidas = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

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

from app import login
from app import cadastro
from app import visualizar

app.include_router(login.router)
app.include_router(cadastro.router)
app.include_router(visualizar.router)
from app import nome_tabelas  
app.include_router(nome_tabelas.router)
from app import praticas
app.include_router(praticas.router)
from app import upload_foto
app.include_router(upload_foto.router)
from fastapi.staticfiles import StaticFiles

app.mount("/fotos", StaticFiles(directory="app/fotos"), name="fotos")
from app import turno
app.include_router(turno.router)
from app import lider
app.include_router(lider.router)
from app.rotas import instrutor_atual
app.include_router(instrutor_atual.router)
from app.rotas import impressao
app.include_router(impressao.router)
from app import subs  
app.include_router(subs.router)
from app import quantos
app.include_router(quantos.router)
from app import anuncios
app.include_router(anuncios.router)
from app import suplente
app.include_router(suplente.router)
from app import senha
app.include_router(senha.router)

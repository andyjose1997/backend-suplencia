from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

# ✅ Modelo de Instrutor
class Instrutor(Base):
    __tablename__ = "instrutores"

    id = Column(String(10), primary_key=True, index=True)
    instrutor = Column(String(100), unique=True, nullable=False)
    link_zoom = Column(String(255), nullable=True)

    espanhol = Column(Boolean, default=False)
    portugues = Column(Boolean, default=False)
    ingles = Column(Boolean, default=False)
    frances = Column(Boolean, default=False)
    japones = Column(Boolean, default=False)
    italiano = Column(Boolean, default=False)

    senha = Column(String(255), nullable=False)
    funcao = Column(String(50), nullable=False)
    colina = Column(Integer, default=0)
    coluna_impressao = Column(Integer, default=0)

    ate = Column(String(10), default="--")
    sub = Column(Integer, default=0)

    supervisor = Column(String(255), nullable=True, default="0")


# ✅ Modelo de Prática
class PraticaGeral(Base):
    __tablename__ = "praticas_geral"

    id = Column(String(10), primary_key=True, index=True)
    turno = Column(String(10))         # manha, tarde, noite
    tipo = Column(String(1))           # 'A' ou 'B'

    # Campos da prática A
    instrutor_A = Column(String(100))
    link_A = Column(String(255))
    sala_A = Column(String(20))
    horario_A = Column(String(10))
    idioma_A = Column(String(50))
    disponibilidade_A = Column(String(50))
    subs_A = Column(Integer)

    # Campos da prática B
    instrutor_B = Column(String(100))
    link_B = Column(String(255))
    sala_B = Column(String(20))
    horario_B = Column(String(10))
    idioma_B = Column(String(50))
    disponibilidade_B = Column(String(50))
    subs_B = Column(Integer)


# ✅ Modelo de Impressão
class Impressao(Base):
    __tablename__ = "impressoes"

    id = Column(Integer, primary_key=True, index=True)
    sala = Column(String(10), nullable=False)
    instrutor = Column(String(100), nullable=False)
    pode_imprimir = Column(Boolean, nullable=False)
    faltou = Column(Boolean, nullable=False)
    observacoes = Column(String(255), nullable=True)
    entregue = Column(Boolean, default=False)
    ate = Column(String(10), default="--")
    sub = Column(Integer, default=0)


# ✅ Modelo de Anúncio
class Anuncio(Base):
    __tablename__ = "anuncios"

    id = Column(Integer, primary_key=True, index=True)
    conteudo = Column(String(500), nullable=False)


# ✅ Modelo de Suplente Atual
class SuplenteAtual(Base):
    __tablename__ = "suplente_atual"

    id = Column(String(36), primary_key=True, index=True)

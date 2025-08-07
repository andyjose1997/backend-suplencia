from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔐 Credenciais do MySQL fornecidas pelo freesqldatabase.com
DB_USER = "sql5794088"
DB_PASSWORD = "FRGkqV3adJ"
DB_HOST = "sql5.freesqldatabase.com"
DB_PORT = "3306"
DB_NAME = "sql5794088"

# 🔗 URL de conexão (com PyMySQL)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 🚀 Engine e sessão
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📦 Base para os modelos
Base = declarative_base()

# ✅ Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

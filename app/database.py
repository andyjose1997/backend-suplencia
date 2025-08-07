from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔐 Credenciais do MySQL
DB_USER = "root"
DB_PASSWORD = "26374246"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "informacoes"

# 🔗 URL de conexão
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 🚀 Engine e sessão
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📦 Base para os modelos
Base = declarative_base()

# ✅ Adicione esta função aqui
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

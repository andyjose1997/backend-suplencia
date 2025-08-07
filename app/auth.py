from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Segredo para assinar o token (pode ser qualquer string segura)
SECRET_KEY = "chave-super-secreta"
ALGORITHM = "HS256"
TEMPO_EXPIRACAO_MINUTOS = 60 * 24  # 1 dia

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha_pura: str, senha_hash: str):
    return pwd_context.verify(senha_pura, senha_hash)

def criar_token_acesso(dados: dict):
    dados_para_token = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=TEMPO_EXPIRACAO_MINUTOS)
    dados_para_token.update({"exp": expira})
    return jwt.encode(dados_para_token, SECRET_KEY, algorithm=ALGORITHM)

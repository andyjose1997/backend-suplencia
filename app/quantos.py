from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor

router = APIRouter()

def horario_para_minutos(horario: str) -> int:
    try:
        h, m = map(int, horario.split(":"))
        return h * 60 + m
    except:
        return -1

@router.get("/disponiveis")
def contar_disponiveis(idioma: str, horario: str, planilha: str = "A", db: Session = Depends(get_db)):
    if not idioma or not horario:
        raise HTTPException(status_code=400, detail="Idioma e horário são obrigatórios")

    idioma = idioma.lower()
    if idioma not in ["portugues", "ingles", "espanhol", "japones", "frances", "italiano"]:
        raise HTTPException(status_code=400, detail="Idioma inválido")

    minutos_referencia = horario_para_minutos(horario)
    if minutos_referencia == -1:
        raise HTTPException(status_code=400, detail="Formato de horário inválido")

    if planilha.upper() == "A":
        instrutores = db.query(Instrutor).filter(
            getattr(Instrutor, idioma) == True,
            Instrutor.sub == 1
        ).all()

        total = len(instrutores)
        subtrair = 0

        for instrutor in instrutores:
            if instrutor.ate:
                minutos_ate = horario_para_minutos(instrutor.ate)
                if minutos_ate <= minutos_referencia:
                    subtrair += 1

        return {"disponiveis": total - subtrair}

    elif planilha.upper() == "B":
        return {"disponiveis": 0}

    else:
        raise HTTPException(status_code=400, detail="Planilha inválida: use A ou B")

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instrutor
from PIL import Image
import os
import shutil
import glob

router = APIRouter()

CAMINHO_FOTOS = os.path.abspath("app/fotos")

@router.post("/upload-foto")
async def upload_foto(file: UploadFile = File(...), nome: str = Form(...), db: Session = Depends(get_db)):
    try:
        print("📂 Upload de:", nome)
        if not os.path.exists(CAMINHO_FOTOS):
            os.makedirs(CAMINHO_FOTOS)

        nome_sanitizado = nome.strip().replace(" ", "_").lower()
        nome_arquivo_final = f"{nome_sanitizado}.jpg"
        caminho_final = os.path.join(CAMINHO_FOTOS, nome_arquivo_final)

        # Salva temporariamente o arquivo
        temp_path = os.path.join(CAMINHO_FOTOS, f"temp_{nome_sanitizado}")
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Converte para JPG
        img = Image.open(temp_path).convert("RGB")
        img.save(caminho_final, "JPEG")
        os.remove(temp_path)

        # Atualiza no banco
        instrutor = db.query(Instrutor).filter(Instrutor.instrutor == nome).first()
        if instrutor:
            instrutor.foto = nome_arquivo_final
            db.commit()

        return {"mensagem": "Foto salva como JPG com sucesso."}

    except Exception as e:
        print("❌ Erro ao salvar imagem:", e)
        raise HTTPException(status_code=500, detail="Erro ao salvar a imagem.")

@router.delete("/apagar-foto/{nome}")
def apagar_foto(nome: str, db: Session = Depends(get_db)):
    try:
        nome_sanitizado = nome.strip().replace(" ", "_").lower()
        padrao = os.path.join(CAMINHO_FOTOS, f"{nome_sanitizado}.jpg")
        
        if not os.path.exists(padrao):
            raise HTTPException(status_code=404, detail="Foto não encontrada")

        os.remove(padrao)
        print(f"🗑️ Foto removida: {padrao}")

        # Atualiza no banco
        instrutor = db.query(Instrutor).filter(Instrutor.instrutor == nome).first()
        if instrutor:
            instrutor.foto = None
            db.commit()

        return {"mensagem": "Foto apagada com sucesso."}

    except Exception as e:
        print("❌ Erro ao apagar imagem:", e)
        raise HTTPException(status_code=500, detail="Erro ao apagar a imagem.")

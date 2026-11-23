from sqlalchemy.orm import sessionmaker
from database import db
from fastapi import Depends, HTTPException
from database import Usuario, Instrutor
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from config import ALGORITHM, ACESS_TOKEN_EXPIREM, SECRET_KEY, oauth2_instrutor, oauth2_usuario


def sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def CriarAcessToken(id_usuario):
    dataexpericao = datetime.now(timezone.utc -3) + timedelta(minutes= ACESS_TOKEN_EXPIREM)
    dicinfo={
        "sub" : id_usuario,
        "exp": dataexpericao
    }
    tokenaccess = jwt.encode(dicinfo, SECRET_KEY, ALGORITHM)

    return tokenaccess

def CriarRefreshToken(id_usuario):
    dataexpericao = datetime.now(timezone.utc -3) + relativedelta(months= 3)
    dictinfo={
        "sub" : id_usuario,
        "exp": dataexpericao
    }
    tokenrefresh = jwt.encode(dictinfo, SECRET_KEY, ALGORITHM)

    return tokenrefresh
    


def VerificarTokenUsuario(token: str = Depends(oauth2_usuario), session = Depends(sessao)):
    try:
        dictinfo = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dictinfo.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado!")

    user= session.query(Usuario).filter(Usuario.id == id_usuario).first()
    
    if not user:
        raise HTTPException(status_code=404, detail=("Usuario não encontrado"))

    return user

def VerificarTokenUsuario(token: str = Depends(oauth2_usuario), session = Depends(sessao)):
    try:
        dictinfo = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dictinfo.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado!")

    instructor= session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not instructor:
        raise HTTPException(status_code=404, detail=("Instrutor não encontrado"))


    return instructor
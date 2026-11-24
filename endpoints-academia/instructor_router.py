from fastapi import HTTPException, Depends,APIRouter
from database import Instrutor
from models import InstrutorEntrada, AlterarPerfil
from config import bcrypt_context
from fastapi.security import OAuth2PasswordRequestForm
from dependecis import sessao, VerificarTokenInstrutor, CriarAccessToken, CriarRefreshToken

instructor_router = APIRouter(tags= ["instructor"])

@instructor_router.get("/instructor", status_code=200)
async def ListarInstrutores(session = Depends(sessao)):
    instrutores = session.query(Instrutor).all()

    return instrutores

@instructor_router.get("/instrutor", status_code=200)


@instructor_router.post("/instrutor", status_code=200)
async def CriarInstrutor(dados: InstrutorEntrada, session = Depends(sessao)):
    instrutor = session.query(Instrutor).filter(Instrutor.email == dados.email).first()

    if instrutor:
        raise HTTPException(status_code=404, detail= "Email já cadastrado!")

    dados.senha = bcrypt_context.hash(dados.senha)

    newinstructor = Instrutor(**dados.model_dump())

    session.add(newinstructor)
    session.commit()
    session.refresh(newinstructor)

    return newinstructor

@instructor_router.post("/instrutor/login", status_code=200)
async def Login(formlogin: OAuth2PasswordRequestForm = Depends(), session= Depends(sessao)):
    instrutor = session.query(Instrutor).filter(Instrutor.email == formlogin.username).first()

    if not instrutor:
        raise HTTPException(status_code=404, detail=("Email ou senha invalidos!"))
    elif not bcrypt_context.verify(formlogin.password, instrutor.senha):
        raise HTTPException(status_code=404, detail="Email ou senha invalido!")

    accesstoken = CriarAccessToken(instrutor.id)
    refreshtoken = CriarRefreshToken(instrutor.id)

    return {
        "access_token": accesstoken,
        "refresh_token":refreshtoken,
        "token_type": "Bearer"
    }

@instructor_router.patch("/instrutor/{instrutor.id}/editarperfil", status_code=200)
async def EditarPerfil(dados: AlterarPerfil, senhaautual: str | None = None, intrustor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    if intrustor.id != id:
        raise HTTPException(status_code=404, detail= "Acesso negado!")

    alteracoes = dados.model_dump(exclude_unset=True)

    if "senha" in alteracoes:
        if not bcrypt_context.verify(senhaautual, intrustor.senha):
            alteracoes["senha"] = bcrypt_context.hash(alteracoes["senha"])

    
    for campo, valor in alteracoes.items():
        setattr(intrustor, campo, valor)

    session.commit()
    session.refresh(intrustor)

    return intrustor

@instructor_router.delete("/instrutor/{instrutor.id}/deletar perfil", status_code=200)
async def ExcluirInstrtutor(id: int, instrutor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    if instrutor.administrador == False:
        raise HTTPException(status_code=404, detail= "Acesso negado!")

    session.delete(instrutor)
    session.commit()

    return{"Exclusão concluída com sucesso"}
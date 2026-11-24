from fastapi import HTTPException, APIRouter,Depends
from dependecis import sessao, VerificarTokenUsuario, CriarAccessToken, CriarRefreshToken
from database import Usuario
from models import UsuarioEntrada, AlterarPerfil
from config import bcrypt_context
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(tags=["user"])

@user_router.get("/usuarios", status_code=200)
async def  ListarUsuarios(session = Depends(sessao)):
    usuarios = session.query(Usuario).all()

    return usuarios

@user_router.get("/usuario/", status_code=200)

@user_router.post("/usuario", status_code=200)
async def Cadastro(dados: UsuarioEntrada, session= Depends(sessao)):
    email = session.query(Usuario).filter(Usuario.email == dados.email).first()

    if email:
        raise HTTPException(409, "email já existe!")

    dados.senha= bcrypt_context.hash(dados.senha)

    newuser = Usuario(**dados.model_dump())

    session.add(newuser)
    session.commit()
    session.refresh(newuser)

    return newuser

@user_router.post("/usuario/login", status_code=200)
async def Login(formlogin: OAuth2PasswordRequestForm = Depends(), session= Depends(sessao)):
    user = session.query(Usuario).filter(Usuario.email == formlogin.username).first()

    if not user:
        raise HTTPException(404, "email ou senha errado!")

    elif not bcrypt_context.verify(formlogin.password, user.senha):
        raise HTTPException(404, "email ou senha errado!")

    accesstoken = CriarAccessToken(user.id)
    refreshtoken = CriarRefreshToken(user.id)

    return {
        "access_token": accesstoken,
        "refresh_token":refreshtoken,
        "token_type": "Bearer"
    }

@user_router.patch("/usuario/{user.id}/perfil", status_code=200)
async def EditarPerfil(dados: AlterarPerfil, senhaautual: str | None = None, user: Usuario = Depends(VerificarTokenUsuario), session = Depends(sessao)):

    if user.id != id:
        raise HTTPException(status_code=401, detail="Acesso negado")

    alteracoes = dados.model_dump(exclude_unset=True)

    if "senha" in alteracoes:
       if not bcrypt_context.verify(senhaautual, user.senha):
            raise HTTPException(400, "Senha atual incorreta!")

       alteracoes["senha"] = bcrypt_context.hash(alteracoes["senha"])

    for campo, valor in alteracoes.items():
        setattr(user, campo, valor)

    session.commit()
    session.refresh(user)

    return user

@user_router.delete("/usuario/{id}/deletarperfil", status_code=200)
async def excluirusuario(id: int, user: Usuario= Depends(VerificarTokenUsuario), session = Depends(sessao)):
    if user.id != id:
        raise HTTPException(404, "Não é possível realizar a ação!")

    u = session.query(Usuario).filter(Usuario.id == id).first()

    session.delete(u)
    session.commit()

    return("usuário excluído com sucesso!")


@user_router.get("/refresh", status_code=200)
async def RenovarRefreshToken(user: Usuario = Depends(VerificarTokenUsuario)):
    refreshtoken = CriarRefreshToken(user.id)

    return {
        "refresh token": refreshtoken,
        "token type": "Bearer"
    }

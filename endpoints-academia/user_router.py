from fastapi import HTTPException, APIRouter,Depends
from dependecis import sessao, VerificarTokenUsuario, CriarAcessToken, CriarRefreshToken
from database import Usuario
from models import UsuarioEntrada
from config import bcrypt_context

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
    session.refrseh(newuser)

    return newuser

@user_router.post("/login", status_code=200)
async def Login(email: str, senha: str, session= Depends(sessao)):
    user = session.query(Usuario).filter(Usuario.email == email and Usuario.senha == senha).first()

    if not user:
        raise HTTPException(404, "email ou senha errado!")

    acesstoken = CriarAcessToken(user.id)
    refreshtoken = refreshtoken(user.id)

    return {
        "acess token": acesstoken,
        "refresh token":refreshtoken,
        "token type": "Bearer"
    }

@user_router.patch("/usuario/{id}/perfil", status_code=200)
async def EditarPerfil(foto: str, nome: str,  telefone: int, senha: str, senhaautual: str, user: Usuario = Depends(VerificarTokenUsuario), session = Depends(sessao)):
    user.foto = foto
    user.nome = nome
    user.telefone = telefone

    if senha:
        if senhaautual == user.senha:
            user.senha = senha

    session.commit()
    session.refresh(user)

    return user

@user_router.delete("/usuario/{id}/deletarperfil", status_code=200)
async def excluirusuario(id_usuario: int, user: Usuario= Depends(VerificarTokenUsuario), session = Depends(sessao)):
    if user.id != id_usuario:
        raise HTTPException(404, "Não é possível realizar a ação!")

    u = session.query(Usuario).filter(Usuario.id == id_usuario).first()

    session.delete(u)
    session.commit()

    return("usuário excluído com sucesso!")


@user_router.get("/refresh", status_code=200)
async def CriarRefreshToken(user: Usuario = Depends(VerificarTokenUsuario)):
    refreshtoken = CriarRefreshToken(user.id)

    return {
        "refresh token": refreshtoken,
        "token type": "Bearer"
    }

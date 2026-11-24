from fastapi import HTTPException, Depends, APIRouter
from dependecis import sessao
from database import Plano
from models import PlanoEntrada

plan_router = APIRouter(tags=["plan"])

@plan_router.get("/plans", status_code=200)
async def ListarPlanos(session = Depends(sessao)):
    planos = session.quey(Plano).all

    return planos

@plan_router.get("/plan", status_code=200)


@plan_router.post("plan", status_code=200)
async def CriarPlano(dados: PlanoEntrada, session = Depends(sessao)):
    
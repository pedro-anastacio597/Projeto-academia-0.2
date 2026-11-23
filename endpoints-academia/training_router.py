from fastapi import HTTPException, APIRouter, Depends
from database import Treino
from dependecis import sessao

training_router = APIRouter(tags=["trainings"])


@training_router.get("/treino", status_code=200)
async def listar_treinos(session = Depends(sessao)):
    treinos = session.query(Treino).all()
     
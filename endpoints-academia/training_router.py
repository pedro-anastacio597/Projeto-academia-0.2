from fastapi import HTTPException, APIRouter, Depends
from database import Treino, Instrutor, Usuario, Treino_Exercicio, Treino_Usuario
from models import TreinoEntrada, AlterarTreino
from dependecis import sessao, VerificarTokenInstrutor, VerificarTokenUsuarioOuInstrutor
from verifications import VerificarExercicio, VerificarTreino, VerificarTreinoExercicio

training_router = APIRouter(tags=["trainings"])


@training_router.get("/treino", status_code=200)
async def listar_treinos(session = Depends(sessao), instrtutor: Instrutor = Depends(VerificarTokenInstrutor)):
    if not instrtutor:
        raise HTTPException(status_code=404, detail=("Acesso negado!"))
    
    treinos = session.query(Treino).all()

    return treinos


@training_router.get("/training/usuer/{id}", status_code=200)
async def BuscarTreino(id_usuario, user = Depends(VerificarTokenUsuarioOuInstrutor), session = Depends(sessao)):
    tabelatreino = session.query(Treino).join(Treino_Usuario, Treino_Usuario.id == Treino.id).filter(Treino_Usuario.id_usuario == id_usuario).all()

    return tabelatreino

@training_router.post("/traning", status_code=200)
async def CriarTreino(dados: TreinoEntrada, instrutor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    if not instrutor:
        raise HTTPException(status_code=404, detail= "Acesso negado!")

    newtraining = Treino(**dados.model_dump())

    session.add(newtraining)
    session.commit()
    session.refresh(newtraining)

    return newtraining

@training_router.patch("/training/{id}/alteratreino", status_code=200)
async def AlterarTreino(id: int,dados: AlterarTreino, instrutor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    if not instrutor:
        raise HTTPException(status_code=404, detail= "Acesso negado")

    treino = VerificarTreino(id, session)
    alteracoes = dados.model_dump(exclude_unset=True)

    for campo, valor in alteracoes.items():
        setattr(treino, campo, valor)

    session.commit()

    session.refresh(treino)

    return treino

@training_router.post("/training/{id_treino}/exrcicio/{id_exercicio}")
async def AdicionarExercicio(id_treino: int, id_exercicio: int, instrutor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    treino = VerificarTreino(id_treino, session)
    exercicio = VerificarExercicio(id_exercicio, session)

    if not treino or not exercicio:
            raise HTTPException(status_code=404, detail="Adicione treino e exericios validos!")

    elif VerificarTreinoExercicio(id_treino, id_exercicio, session):
            raise HTTPException(status_code=409, detail="Exercico já existe neste treino!")
    
    treinoexercicio = Treino_Exercicio(id_treino= id_treino, id_exercicio= id_exercicio)


    session.add(treinoexercicio)
    session.commit()
    session.refresh(treinoexercicio)

    return treinoexercicio

@training_router.delete("/training/{id_treino}/exrcicio/{id_exercicio}")
async def ExcluirExercicio(id_treino: int, id_exercicio: int, instrutor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    treino = VerificarTreino(id_treino, session)
    exercicio = VerificarExercicio(id_exercicio, session)

    if not treino or not exercicio:
        raise HTTPException(status_code=404, detail="Adicione treino e exericios validos!")

    treinoexercicio = VerificarTreinoExercicio(id_treino, id_exercicio, session)

    if not treinoexercicio:
            raise HTTPException(status_code=409, detail="Exercico não existe neste treino!")

    session.delete(treinoexercicio)
    session.commit()

    return{"Exercicio removido do treino com sucesso!"}



    
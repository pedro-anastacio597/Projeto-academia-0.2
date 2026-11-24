from fastapi import HTTPException
from database import Instrutor, Usuario, Treino, Exercicio, Treino_Exercicio

def VerificarExcluir(id: int, instrutor: Instrutor | None = None, user: Usuario | None = None):
    if instrutor:
        if instrutor.administrador == False and id:
            raise HTTPException(status_code=404, detail= "Acesso negado")

    elif user:
        if user.id != id:
            raise HTTPException(status_code=404, detail= "Acesso negado")

    elif not user and not instrutor:
        raise HTTPException(status_code=404, detail= "Envie um usuario ou instrutor")

    return True

def VerificarTreino(id, session):
    treino = session.query(Treino).filter(Treino.id == id).first()

    return treino

def VerificarExercicio(id, session):
    exercicio = session.query(Exercicio).filter(Exercicio.id ==  id).first()

    return exercicio

def VerificarTreinoExercicio(id_treino, id_exercicio, session):
    treinoexercicio = session.query(Treino_Exercicio).filter(Treino_Exercicio.id == id_treino, Treino_Exercicio.id == id_exercicio)

    return treinoexercicio
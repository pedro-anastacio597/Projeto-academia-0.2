from fastapi import Depends, HTTPException, APIRouter
from database import Matricula, Usuario, Instrutor
from models import MatriculaEntrada, AltrarMatricula
from dependecis import sessao, VerificarTokenInstrutor, VerificarTokenUsuarioOuInstrutor, VerificarTokenUsuario
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from verifications import VerificarMatricula

matriculation_router = APIRouter(tags=["matriculation"])

@matriculation_router.get("/matriculation/{user.id_usuario}", status_code=200)
async def BuscarMatricular(user: Usuario= Depends(VerificarTokenUsuarioOuInstrutor), session = Depends(sessao)):
    matricula = session.query(Matricula).filter(Matricula.id_usuario == user.id)

    return matricula

@matriculation_router.post("/matriculation", status_code=200)
async def CriarMatricula(dados: MatriculaEntrada, datavencimento: str, datapagamento: str, instrutor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    if not instrutor:
        raise HTTPException(status_code=404, detail= "Acesso negado")

    m = session.query(Matricula).filter(Matricula.id_usuario == dados.id_usuario).first()

    if m:
        raise HTTPException(status_code=404, detail="Matricula já existe!")
    
    dataatual = datetime.now()

    data = dataatual.date()

    dataincio = data.strftime("%d/%m/%Y")

    duracao = dados.id_plano.duracao.split()

    anos = 0
    meses = 0
    dias = 0

    for i, parte in enumerate(duracao):
        if i == "ano" or "anos":
            anos = int(duracao[parte-1])

        elif i == "mes" or "meses" == i:
            meses = int(duracao[parte-1])

        elif i == "semana" or i =="semanas":
            dias = int(duracao[parte-1]) * 7

        elif i == "dia" or i =="dias":
            dias = int(duracao[parte-1])

    datavencimento = data + relativedelta(years= anos, months= meses, days= dias)

    datavencimentoformatada = datavencimento.strftime("%d/%m/%Y")

    if not datapagamento:
        datapagamento = None
    if datapagamento:
        datapagamento = dataincio

    novamatricula = Matricula(**dados.model_dump(), data_inicio= dataincio, data_vencimento= datavencimentoformatada, datapagamento = datapagamento)

    return novamatricula


@matriculation_router.patch("/matriculation/{id}", status_code=200)
async def Renovar(id: int, instrutor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    if not instrutor:
        raise HTTPException(status_code=404, detail= "Acesso negado")

    matricula = VerificarMatricula(id, session)

    if not matricula:
        raise HTTPException(status_code=404, detail="Matricula não encontrada!")

    dataatual = datetime.now()
    
    data = dataatual.date()

    datapagamento = data.strftime("%d/%m/%Y")

    matricula.data_pagamento = datapagamento

    session.commit()
    session.refresh(matricula)

    return matricula

@matriculation_router.patch("/matriculation/{user.id_usuario}")
async def AlterarMatricula(dados: MatriculaEntrada, user: Usuario = Depends(VerificarTokenUsuario), session = Depends(sessao)):
    if  

@matriculation_router.post("/matriculation/{matricula.id_usuario}/Alterarstutas", status_code=200)
async def Desativarconta(matricula: Matricula, instrutor: Instrutor = Depends(VerificarTokenInstrutor), session = Depends(sessao)):
    if not instrutor:
        raise HTTPException(status_code=404, detail="Acesso negado")

    matricula.status("Cancelado")

    return matricula


@matriculation_router.delete("/matriculation/{id}/Excluir", status_code=200)
async def ExcluirMatricula(id: int, user: Usuario = Depends(VerificarTokenUsuario), session =Depends(sessao)):
    matricula = VerificarMatricula(id, session)

    if not matricula:
        raise HTTPException(status_code=404, detail="A matricula não existe!")

    if matricula.id_usuario != user.id:
        raise HTTPException(status_code=404, detail="Acesso negado!")

    session.delete(matricula)
    session.commit()

    return{"Matricula excluida com sucesso!"}

    
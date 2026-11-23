from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import declarative_base, relationship

db= create_engine("sqlite:///banco.db")
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=True)
    email = Column("email", String, nullable=True, unique=True)
    senha= Column("senha", String, nullable=True)
    telefone= Column("telefone", Integer)
    sexo= Column("sexo", String)
    foto= Column("foto", String)


    "matricula" = relationship(
        "matricula",
        back_populates= "usuario",
        cascade= "all"
    )

    "treino_aluno" = relationship(
        "treino_aluno",
        back_populates= "usuario",
        cascade= "all"
    )


    def __init__(self, nome, email, senha, sexo, telefone = None, foto = None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.sexo = sexo
        self.foto = foto


class Instrutor(Base):
    _tablename__ = "instrutor"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=True)
    email = Column("email", String, nullable=True, unique=True)
    senha= Column("senha", String, nullable=True)
    Telefone= Column("telefone", Integer, nullable=True)

    "alteracao_treino" = relationship(
        "alteracao_treino",
        back_populates="instrutor"
    )

    def __init__(self, nome, email, senha, telefone = None):
            self.nome = nome
            self.email = email
            self.senha = senha
            self.telefone = telefone

class Treino(Base):
    __tablename__ = "treino"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=True)
    objetivo = Column("objetivo", String)
    descricao = Column("descricao", String)

    "treino_exercicio" = relationship(
        "treino_exercicio",
        back_populates= "treino",
        cascade= "all"
    )

    "treino_usuario" = relationship(
        "treino_usuario",
        back_populates= "treino",
        cascade= "all"
    )

    "alteracao_treino" = relationship(
        "alteracao_treino",
        back_populates="treino",
        cascade= "all"
    )

    def __init__(self, nome, objetivo, descricao = None):
         self.nome = nome
         self.objetivo = objetivo
         self.descricao = descricao


class Exercico(Base):
    __tablename__ = "exercicio"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=True)
    grupo = Column("grupo", String, nullable=True)
    imagem = Column("imagem", String, nullable=True)
    video = Column("video", String)

    series = relationship(
        "series",
        cascade= "all",
        back_populates= "exercicio"
    )

    "treino_exercicio" = relationship(
        "treino_exercicio",
        back_populates= "exercicio",
        cascade= "all"
    )

    def __init__(self, nome, grupo, imagem, video = None):
        self.nome = nome
        self.grupo = grupo
        self.imagem =  imagem
        self.video = video

class Series(Base):
    __tablename__ = "sereis"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    numero = Column("numero", Integer, nullable=True)
    peso = Column("peso", float, default= 0)
    id_exercicio = Column("id_exercicio", Integer, ForeignKey("exercicio.id"))

    exercicio = relationship(
        "exercicio",
        back_populates= "series"
    )

class Plano(Base):
    __tablename__ = "plano"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=True)
    valor = Column("valor", float, nullable=True)
    descricao = Column("descricao", String, nullable=True)
    duracao = Column("duracao", String, nullable=True)

    "matricula" = relationship(
        "matricula",
        back_populates= "plano"
    )

    def __init__(self, nome, valor, descricao, duracao):
         self.nome = nome
         self.valor = valor
         self.descricao = descricao
         self.duracao = duracao


class Matricula(Base):
    __tablename__ = "matricula"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("usuario.id"), nullable=True)
    id_plano = Column("id_plano", Integer, ForeignKey("plano.id"), nullable=True)
    status = Column("status", String, nullable=True)
    data_inicio = Column("data_inicio", Date)
    data_vencimento = Column("data_vencimento", Date, nullable=True)
    data_pagamento = Column("data_pagamento", Date, default= None)

    "usuario" = relationship(
        "usuario",
        back_populates= "matricula"
    )

    def __init__(self, id_usuario, id_plano, data_inicio, data_vencimento, status = "ativo", ):
        self.id_usuario = id_usuario
        self.id_palno = id_plano
        self.data_inicio = data_inicio
        self.data_vencimento = data_vencimento
        self.status = status

class Treino_Exercicio(Base):
    __tablename__ = "treino_exercicio"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_treino = Column("id_treino", Integer, ForeignKey("treino.id"), nullable=True)
    id_exercicio = Column("id_exercicio", Integer, ForeignKey("exercicio.id"), nullable=True)

    "treino" = relationship(
        "treino",
        back_populates= "treino_exercicio"
    )

    "exercicio" = relationship(
        "exercicio",
        back_populates= "treino_exercicio"
    )

    def __init__(self, id_treino, id_exercicio):
        self.id_treino = id_treino
        self.id_exercicio = id_exercicio

class Treino_usuario(Base):
    __tablename__ = "treino_exercicio"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_treino = Column("id_treino", Integer, ForeignKey("treino.id"), nullable=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("usuario.id"), nullable=True)

    "exercicio" = relationship(
        "exercicio",
        back_populates= "treino_usuario"
    )

    "usuario" = relationship(
        "usuario",
        back_populates= "treino_usuario"
    )

    def __init__(self, id_treino, id_usuario):
        self.id_treino = id_treino
        self.id_usuario = id_usuario 

class Alteracao_treino (Base):
    __tablename__ = "alteracao_treino"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_treino = Column("id_treino", Integer, ForeignKey("treino.id"), nullable=True)
    id_instrutor = Column("id_instrutor", Integer, ForeignKey("instrutor.id"), nullable=True)
    data_alteracao = Column("data_alteracao", Date, nullable=True,)

    "instrutor" = relationship(
        "instrutor",
        back_populates= "alteracao_treino"
    )

    "treino" = relationship(
            "treino",
            back_populates= "alteracao_treino"
        )

    def __init__(self, id_treino, id_instrutor):
        self.id_treino = id_treino
        self.id_instrutor = id_instrutor
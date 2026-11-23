from pydantic import BaseModel, EmailStr, dataclasses

class UsuarioEntrada(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    sexo: str
    telefone: int | None = None
    foto: str | None = None

class InstrutorEntrada(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    telefone: int

class ExercicioEntrada(BaseModel):
    nome: str
    grupo: str
    imagem: str
    video: str | None = None

class SerieEntrada(BaseModel):
    numero: int
    peso: float 
    id_exercicio: int

class TreinoEntrada(BaseModel):
    nome: str
    objetivo: str
    descricao: str

class MatriculaEntrada(BaseModel):
    id_usuario: int
    id_plano: int
    status: str